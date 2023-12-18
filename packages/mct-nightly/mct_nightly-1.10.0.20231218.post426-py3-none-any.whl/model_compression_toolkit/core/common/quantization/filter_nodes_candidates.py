# Copyright 2022 Sony Semiconductor Israel, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import copy
from typing import List

from model_compression_toolkit.target_platform_capabilities.target_platform import QuantizationMethod

from model_compression_toolkit.core.common import Graph, BaseNode
from model_compression_toolkit.constants import FLOAT_BITWIDTH
from model_compression_toolkit.core.common.quantization.candidate_node_quantization_config import \
    CandidateNodeQuantizationConfig


def filter_nodes_candidates(graph: Graph):
    """
    Filters the graph's nodes candidates configuration list.
    We apply this after mark activation operation to eliminate nodes that their activation are no longer being quantized
    from the mixed-precision search.
    Updating the lists is preformed inplace on the graph object.

    Args:
        graph: Graph for which to add quantization info to each node.
    """
    nodes = list(graph.nodes)
    for n in nodes:
        n.candidates_quantization_cfg = filter_node_candidates(node=n)

    return graph


def _filter_bit_method_dups(candidates: List[CandidateNodeQuantizationConfig]) -> List[CandidateNodeQuantizationConfig]:
    """
    Filters out duplications in candidates configuration list, based on similarity in
    (weights_n_bits, weights_quantization_method, activation_n_bits, activation_quantization_method).

    Args:
        candidates: A list of quantization configuration candidates.

    Returns: A filtered list of quantization configuration candidates.

    """
    seen_bits_method_combinations = set()
    final_candidates = []
    for c in candidates:
        comb = (c.weights_quantization_cfg.weights_n_bits,
                c.weights_quantization_cfg.weights_quantization_method,
                c.activation_quantization_cfg.activation_n_bits,
                c.activation_quantization_cfg.activation_quantization_method)
        if comb not in seen_bits_method_combinations:
            final_candidates.append(c)
            seen_bits_method_combinations.add(comb)

    return final_candidates


def filter_node_candidates(node: BaseNode) -> List[CandidateNodeQuantizationConfig]:
    """
    Updates a node's candidates configuration list.
    If the node's weights quantization is disabled (or it only has activations to quantize), then the updated list
    will have a candidate with any of the different original activation bitwidths candidates and a default value
    for its weights bitwidth (that doesn't have any impact on the quantization or the mixed-precision search.
    If the node's activation quantization is disabled, the same filtering applied for the weights bitwidth candidates.

    Args:
        node: Node to set its quantization configurations.
    """

    filtered_candidates = copy.deepcopy(node.candidates_quantization_cfg)
    final_candidates = copy.deepcopy(node.candidates_quantization_cfg)

    if not node.is_weights_quantization_enabled() and not node.is_activation_quantization_enabled():
        # If both weights and activation quantization are disabled, but for some reason the node has multiple candidates
        # then replace it with a single dummy candidate with default bit-width values.
        single_dummy_candidate = filtered_candidates[0]
        single_dummy_candidate.activation_quantization_cfg.activation_n_bits = FLOAT_BITWIDTH
        single_dummy_candidate.weights_quantization_cfg.weights_n_bits = FLOAT_BITWIDTH
        single_dummy_candidate.weights_quantization_cfg.weights_quantization_method = QuantizationMethod.POWER_OF_TWO
        single_dummy_candidate.activation_quantization_cfg.activation_quantization_method = QuantizationMethod.POWER_OF_TWO
        final_candidates = [single_dummy_candidate]

    elif not node.is_activation_quantization_enabled():
        # Remove candidates that have duplicated weights candidates for node with disabled activation quantization.
        # Replacing the activation n_bits in the remained configurations with default value to prevent confusion.
        seen_candidates = set()
        filtered_candidates = [candidate for candidate in filtered_candidates if
                               candidate.weights_quantization_cfg not in seen_candidates
                               and not seen_candidates.add(candidate.weights_quantization_cfg)]

        for c in filtered_candidates:
            c.activation_quantization_cfg.activation_n_bits = FLOAT_BITWIDTH
            c.activation_quantization_cfg.activation_quantization_method = QuantizationMethod.POWER_OF_TWO

        final_candidates = _filter_bit_method_dups(filtered_candidates)

    elif not node.is_weights_quantization_enabled():
        # Remove candidates that have duplicated activation candidates for node with disabled weights quantization.
        # Replacing the weights n_bits in the remained configurations with default value to prevent confusion.
        seen_candidates = set()
        filtered_candidates = [candidate for candidate in filtered_candidates if
                               candidate.activation_quantization_cfg not in seen_candidates
                               and not seen_candidates.add(candidate.activation_quantization_cfg)]

        for c in filtered_candidates:
            c.weights_quantization_cfg.weights_n_bits = FLOAT_BITWIDTH
            c.weights_quantization_cfg.weights_quantization_method = QuantizationMethod.POWER_OF_TWO

        final_candidates = _filter_bit_method_dups(filtered_candidates)

    return final_candidates
