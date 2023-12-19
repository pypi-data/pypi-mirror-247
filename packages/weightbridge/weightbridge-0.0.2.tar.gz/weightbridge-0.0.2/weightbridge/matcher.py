
import numpy as np
import time, types, traceback, os, json
from collections import defaultdict
from . import tree
from .matchers.base import Match
from . import matchers
from functools import partial
from .state import State

LOAD_PREFIX = "load_prefix"
CACHE_VERSION = 1

possible_separators = ["/", "."]
def get_separator_for(names, type):
    has_separator = [any(s in name for name in names) for s in possible_separators]
    n = np.count_nonzero(has_separator)
    if n == 0:
        return None
    elif n == 1:
        return possible_separators[np.argmax(has_separator, axis=0)]
    else:
        raise ValueError(f"Could not implicitly determine separator in weight names. Please provide argument {type}.")


def _cache_key(x):
    result = []
    for k, v in x.items():
        result.append([
            k,
            list(v.shape),
        ])
    return result

def adapt(in_values, out_values, in_format=None, out_format=None, in_separator=None, out_separator=None, hints=[], cache=None, verbose=False):
    t0 = time.time()
    if isinstance(out_values, dict):
        single_input = True
        out_values = [out_values]
    if isinstance(in_values, dict):
        in_values = [in_values]

    # Get separator in input values
    if in_separator is None:
        keys = set()
        def recurse(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    keys.add(k)
                    recurse(v)
        for d in in_values:
            recurse(d)
        in_separator = get_separator_for(keys, "in_separator")
        if in_separator is None:
            in_separator = possible_separators[0]

    # Get separator in output values
    if out_separator is None:
        keys = set()
        def recurse(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    keys.add(k)
                    recurse(v)
        for d in out_values:
            recurse(d)
        out_separator = get_separator_for(keys, "out_separator")
        if out_separator is None:
            out_separator = possible_separators[0]

    # Flatten input values
    flat_in_values = {}
    def recurse(source, key=()):
        if isinstance(source, dict):
            for k, v in source.items():
                recurse(v, key + (k,))
        else:
            if len(key) == 0:
                raise ValueError("Input values must be a dictionary")
            name = in_separator.join(key)
            if name in flat_in_values:
                raise ValueError(f"Duplicate input name {name}")
            flat_in_values[name] = np.asarray(source)
    for d in in_values:
        recurse(d)
    in_values = flat_in_values

    # Flatten output values and remember tree structure
    flat_out_values = {}
    def recurse(source, key=()):
        if isinstance(source, dict):
            treedef = {}
            for k, v in source.items():
                treedef[k] = recurse(v, key + (k,))
            return treedef
        else:
            if len(key) == 0:
                raise ValueError("Output values must be a dictionary")
            name = out_separator.join(key)
            if name in flat_out_values:
                raise ValueError(f"Duplicate output name {name}")
            source = types.SimpleNamespace(shape=tuple(source.shape), dtype=str(source.dtype))
            flat_out_values[name] = source
            return (name, source.shape, source.dtype)
    out_treedefs = []
    for d in out_values:
        out_treedefs.append(recurse(d))
    out_values = flat_out_values

    state = State(
        in_values,
        {LOAD_PREFIX + out_separator + k: v for k, v in out_values.items()},
        in_separator=in_separator,
        out_separator=out_separator,
        in_format=in_format,
        out_format=out_format,
        hints=hints,
        verbose=verbose,
    )

    # Build module trees
    out_tree = tree.build(state.out_values)
    in_tree = tree.build(state.in_values)
    # Check if mapping is cached
    cache_miss = True
    if not cache is None:
        if not cache.endswith(".json"):
            cache += ".json"
        if not os.path.isabs(cache):
            stack = traceback.extract_stack()
            assert len(stack) >= 2
            path, _, _, _ = stack[-2]
            path = os.path.dirname(path)
            cache = os.path.join(path, cache)

        cache_key = [
            CACHE_VERSION,
            _cache_key(in_values),
            _cache_key(out_values),
            in_format,
            out_format,
            in_separator,
            out_separator,
        ]

        if os.path.isfile(cache):
            with open(cache, "r") as f:
                data = json.load(f)
            if not data is None and "key" in data and "mapping" in data and data["key"] == cache_key:
                if verbose:
                    print("Found cache file, and it matches the input data. Loading mapping.")
                cache_miss = False

                in_nodes = {node.full_prefix: node for node in in_tree}
                out_nodes = {node.full_prefix: node for node in out_tree}

                for out_name, in_name in data["mapping"]:
                    state.pair_node(in_nodes[in_name], out_nodes[out_name])
            else:
                if verbose:
                    print("Found cache file, but it doesnot match the input data. Rerunning matching.")
        else:
            if verbose:
                print("Found no cache file. Running matching.")

    if cache_miss:
        # Initialize matches
        matches = [Match(list(in_tree), list(out_tree), "Root")]

        # Construct heuristics
        ops = [
            partial(matchers.match_by_structured_shapes.match_by_structured_shapes, format="product"),
            partial(matchers.match_by_structured_shapes.match_by_structured_shapes, format="as-input-shape"),
            partial(matchers.match_by_structured_shapes.match_by_structured_shapes, format="as-output-shape"),
            matchers.match_by_paired_parents.match_by_paired_parents,
            matchers.match_by_paired_children.match_by_paired_children,
            matchers.match_unique_leafs.match_unique_leafs,
            matchers.match_number_regex.match_number_regex,
            matchers.match_known_paired_number_regex.match_known_paired_number_regex,
            matchers.match_equivalent_hardcoded_leafs.match_equivalent_hardcoded_leafs,
            matchers.match_passed_hints.match_passed_hints,
            matchers.match_by_paired_prefixes.match_by_paired_prefixes,
            matchers.match_by_paired_predecessors.match_by_paired_predecessors,
        ]
        def op_to_string(op):
            if isinstance(op, partial):
                args = [str(a) for a in op.args] + [f"{k}={v}" for k, v in op.keywords.items()]
                return f"{op.func.__name__}({', '.join(args)})"
            else:
                return op.__name__
        ops = [(op_to_string(op), op) for op in ops]

        # Run matching heuristics
        times = defaultdict(lambda: 0.0)
        changed = True
        while changed:
            changed = False
            for name, op in ops:
                if verbose:
                    print(f"OP: Trying {name}")
                start = time.time()
                matches, changed = op(state, matches)

                times[name] += time.time() - start
                if changed:
                    if verbose:
                        print(f"OP: Changed by {name}")
                    break

        if verbose:
            print("Times (sec) per operation:")
            for k, v in sorted(times.items(), key=lambda t: t[1]):
                print(f"    {k} {v}")

        if len(matches) > 0:
            print()
            for match in matches:
                print("Failed to pair the following nodes")
                for n in match.out_nodes:
                    print(f"    OUT {n.full_prefix} {n.get_structured_shapes()}")
                for n in match.in_nodes:
                    print(f"    IN  {n.full_prefix} {n.get_structured_shapes()}")
            raise ValueError("Failed to pair input values with output values")

        # Check if any hints are unused
        unused_hints = set(state.hints) - set(state.used_hints)
        if len(unused_hints) > 0:
            raise ValueError(f"Unused hints: {unused_hints}")

    # Matching successful!

    # Save to cache
    if not cache is None and cache_miss:
        data = {
            "key": cache_key,
            "mapping": [[out_node.full_prefix, in_node.full_prefix] for out_node, in_node in state.paired_nodes if out_node.is_leaf() and in_node.is_leaf()],
        }
        with open(cache, "w") as f:
            json.dump(data, f)

    if verbose:
        print()
        print("Paired values:")
        mapping = {out_node.full_prefix: in_node for out_node, in_node in state.paired_nodes if out_node.is_leaf() and in_node.is_leaf()}
        for out_value in state.out_values:
            print(f"    {out_value.name} {out_value.shape} -> {mapping[out_value.name].full_prefix} {mapping[out_value.name].value.shape}")

    # Create output dicts from stored tree structure
    out_values_by_name = {v.name: v for v in state.out_values}
    def recurse(x):
        if isinstance(x, dict):
            return {k: recurse(v) for k, v in x.items()}
        else:
            out_name, out_shape, dtype = x
            in_value = out_values_by_name[LOAD_PREFIX + out_separator + out_name].other.value
            in_name = out_values_by_name[LOAD_PREFIX + out_separator + out_name].other.name

            assert np.prod(in_value.shape) == np.prod(out_shape)

            out_value = state.formatter.adapt_format(in_value, out_shape, in_name, out_name)

            return out_value
    out_values = [recurse(treedef) for treedef in out_treedefs]

    if verbose:
        print(f"weightmatcher.adapt took {time.time() - t0:.2f} seconds")

    return out_values[0] if single_input else out_values
