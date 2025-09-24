import time
from .data_structures import ReasoningTree, Fact, FactType
from utils.llm_api import LLM_API

class StoryGenerator:
    """
    Generates a story using chaptering and validates fact recall, a method for ensuring
    factual consistency in long narratives as described in the MuSR paper.
   
    """
    def __init__(self, llm_api: LLM_API):
        self.llm_api = llm_api
        self.chapter_prompt = self._load_prompt("chapter_prompt.txt")
        self.smoother_prompt = self._load_prompt("story_smoother_prompt.txt")
        self.rewrite_prompt = self._load_prompt("story_rewrite_prompt.txt")

    def _load_prompt(self, filename: str) -> str:
        with open(f"prompts/{filename}", 'r', encoding='utf-8') as f:
            return f.read()
            
    def generate_story_with_validation(self, reasoning_tree: ReasoningTree) -> str:
        """Orchestrates the chaptered generation, validation, and potential rewrite."""
        chapters, essential_facts = self._generate_chapters(reasoning_tree)
        draft_story = self._combine_chapters(chapters)

        print("\n[Step 4/6] Validating fact recall in draft story...")
        missing_facts = self._validate_fact_recall(draft_story, essential_facts)

        if not missing_facts:
            print("...All facts recalled successfully. Finalizing story.")
            return draft_story
        else:
            print(f"...Missing {len(missing_facts)} facts. Rewriting story to include them.")
            final_story = self._rewrite_story(draft_story, missing_facts)
            return final_story

    def _generate_chapters(self, reasoning_tree: ReasoningTree) -> (dict, list):
        """Generates a chapter for each main section of the reasoning tree."""
        chapters = {}
        essential_facts = []
        
        intro_facts = self._get_facts_as_string(reasoning_tree.root)
        chapters['introduction'] = self._create_chapter("introduction to the taxpayer", intro_facts)

        for node in reasoning_tree.root.children:
            node_facts = self._get_facts_as_string(node)
            chapter_title = node.description.lower().replace(" ", "_")
            chapters[chapter_title] = self._create_chapter(node.description, node_facts)
            
            for fact in node.facts:
                if fact.type == FactType.NARRATIVE or fact.is_deduction or fact.is_income:
                    essential_facts.append(f"{fact.description}: {fact.value}")
        
        return chapters, essential_facts

    def _create_chapter(self, title: str, facts: str) -> str:
        """Generates a single chapter using the LLM."""
        print(f"  - Generating chapter: {title}")
        if not facts.strip(): return ""
        prompt = self.chapter_prompt.format(chapter_title=title, facts=facts)
        return self.llm_api.generate(prompt)

    def _combine_chapters(self, chapters: dict) -> str:
        """Combines generated chapters into a single story draft."""
        full_text = "\n\n".join(filter(None, chapters.values()))
        prompt = self.smoother_prompt.format(story_chapters=full_text)
        print("\n[Step 3/6] Combining chapters into a cohesive narrative...")
        return self.llm_api.generate(prompt)

    def _validate_fact_recall(self, story: str, essential_facts: list) -> list:
        """Checks if essential facts are present in the story."""
        missing_facts = []
        for fact in essential_facts:
            prompt = f"Read the story below.\n\nSTORY:\n{story}\n\nBased ONLY on the text of the story, does it support the following fact?\nFACT: '{fact}'\n\nAnswer with a single word: YES or NO."
            response = self.llm_api.generate(prompt, system_prompt="You are a precise fact-checker.")
            
            print(f"  - Checking fact: \"{fact[:60]}...\" -> {'PRESENT' if 'yes' in response.lower() else 'MISSING'}")
            if 'no' in response.lower():
                missing_facts.append(fact)
            time.sleep(1) # Avoid hitting API rate limits
        return missing_facts

    def _rewrite_story(self, draft_story: str, missing_facts: list) -> str:
        """Prompts the LLM to rewrite the story to include missing facts."""
        missing_facts_str = "\n".join([f"- {f}" for f in missing_facts])
        prompt = self.rewrite_prompt.format(draft_story=draft_story, missing_facts=missing_facts_str)
        return self.llm_api.generate(prompt)

    def _get_facts_as_string(self, node: object) -> str:
        """Helper to format facts from a node into a string for the LLM."""
        fact_list = []
        for fact in node.facts:
            if fact.type == FactType.NARRATIVE or fact.is_income or fact.is_deduction:
                fact_list.append(f"- {fact.description}: {fact.value}")
        
        for child in node.children:
            fact_list.extend(self._get_facts_as_string(child).splitlines())

        return "\n".join(sorted(list(set(fact_list))))