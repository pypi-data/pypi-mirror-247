from typing import Dict, List, Set, Tuple
import json

class TokenizerPrefixTreeNode:
    def __init__(self):
        self.tokens: List[int] = []
        self.children: Dict[str, TokenizerPrefixTreeNode] = {}


class TokenizerPrefixTree:
    def __init__(self, regular_tokens: List[Tuple[int, str, bool]]):
        self.root = TokenizerPrefixTreeNode()
        self.json_freetext_tokens: List[int] = []
        self.new_word_tokens: Set[int] = set()
        self.tokens_to_strs = {token_idx: token_str for token_idx, token_str, _ in regular_tokens}
        for token_idx, decoded, is_new_word in regular_tokens:
            self._add_token_to_tree(decoded, token_idx, self.root)
            # Performance optimization - cache the tokens of all the strings that don't contain a quote in the middle, or a line break.
            # When we are in a JSON freetext string field, they will all be permitted and this will save a lot of tree iterations.
            has_quote_before_end = '"' in decoded[0:-1]
            has_newline = "\n" in decoded or "\r" in decoded

            if not (has_quote_before_end or has_newline):
                if '\\' in decoded[:-1]:
                    # If there is a backslash that is not trailing, we might be in an illegal json territory. Need to verify
                    # that is is a legal json character streak
                    try:
                        json.loads(f'"{decoded}"')
                    except json.decoder.JSONDecodeError:
                        continue
                self.json_freetext_tokens.append(token_idx)
            if is_new_word:
                self.new_word_tokens.add(token_idx)

    def _add_token_to_tree(self, token_str: str, token_idx: int, node: TokenizerPrefixTreeNode):
        for character in token_str:
            if character not in node.children:
                node.children[character] = TokenizerPrefixTreeNode()
            node = node.children[character]
        node.tokens.append(token_idx)
