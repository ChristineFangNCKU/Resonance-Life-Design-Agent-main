import time
from enum import Enum, auto
from colorama import Fore, Style
from .utils import print_system, print_agent, print_user
from .llm_client import LLMClient
from .matcher import ResonanceMatcher

class AgentState(Enum):
    """[Requirement: State Machine] 定義狀態"""
    INIT = auto()
    Q_VALUES = auto()
    Q_TALENTS = auto()
    Q_DREAMS = auto()
    ANALYZING = auto()
    MATCHING = auto()
    REPORT = auto()

class ResonanceAgent:
    def __init__(self, database, demo_mode=False):
        self.state = AgentState.INIT
        self.db = database
        self.demo_mode = demo_mode
        self.context = []
        self.user_profile = {}
        self.llm_client = LLMClient()
        
        # Demo 預設腳本 (對應 u001 Alex Chen)
        self.demo_script = {
            "values": "I admire Elon Musk and Steve Jobs. I believe in Innovation and creating Impact. I hate inefficiency.",
            "talents": "I get impatient when people make ugly designs or illogical arguments. I am good at Visual Strategy and Pitching.",
            "dreams": "I want to start a Social Enterprise to fix the Education system. I have books like Zero to One on my shelf."
        }

    def get_input(self, question, step_key):
        print_agent(question)
        if self.demo_mode:
            time.sleep(1.0) # 模擬思考時間
            answer = self.demo_script.get(step_key, "...")
            print_user(answer, is_demo=True)
            return answer
        else:
            return input(f"{Fore.YELLOW}[User]: {Style.RESET_ALL}")

    def run(self):
        """狀態機主迴圈"""
        print_system(f"Agent initialized. Mode: {'DEMO' if self.demo_mode else 'INTERACTIVE'}")
        
        while True:
            if self.state == AgentState.INIT:
                print_agent("Welcome to Resonance. Let's find your life partner.")
                self.state = AgentState.Q_VALUES

            elif self.state == AgentState.Q_VALUES:
                ans = self.get_input(
                    "Q1 [Values]: Who do you admire most and why? What principles drive you?", 
                    "values"
                )
                self.context.append(f"Values: {ans}")
                self.state = AgentState.Q_TALENTS

            elif self.state == AgentState.Q_TALENTS:
                ans = self.get_input(
                    "Q2 [Talents]: When do you feel most impatient with others? What comes easy to you?", 
                    "talents"
                )
                self.context.append(f"Talents: {ans}")
                self.state = AgentState.Q_DREAMS

            elif self.state == AgentState.Q_DREAMS:
                ans = self.get_input(
                    "Q3 [Dreams]: What books do you buy? What social problem makes you angry?", 
                    "dreams"
                )
                self.context.append(f"Dreams: {ans}")
                self.state = AgentState.ANALYZING

            elif self.state == AgentState.ANALYZING:
                print_system("Analyzing your soul profile with LLM...")
                self.user_profile = self.llm_client.analyze_user(self.context)
                
                print(f"{Fore.MAGENTA}>> Extracted Values: {self.user_profile.get('core_values')}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}>> Extracted Talents: {self.user_profile.get('top_talents')}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}>> Extracted Dreams: {self.user_profile.get('dream_domain')}{Style.RESET_ALL}")
                self.state = AgentState.MATCHING

            elif self.state == AgentState.MATCHING:
                print_system("Searching database for resonance...")
                self.matches = ResonanceMatcher.find_top_matches(self.user_profile, self.db)
                self.state = AgentState.REPORT

            elif self.state == AgentState.REPORT:
                self.display_results()
                break

    def display_results(self):
        print("\n" + "="*50)
        print(f"{Fore.WHITE} RESONANCE REPORT {Style.RESET_ALL}")
        print("="*50)
        
        if not self.matches or self.matches[0]['score'] == 0:
            print("No strong resonance found.")
            return

        top = self.matches[0]
        c = top['candidate']
        
        print(f"🏆 {Fore.YELLOW}Best Match: {c['name']} ({c['major']}){Style.RESET_ALL}")
        print(f"   Resonance Score: {top['score']}")
        print(f"   Why: {', '.join(top['details'])}")
        print(f"   Summary: {c['interview_summary'][:120]}...")
        print("-" * 50)
        print(f"{Fore.GREEN}Action Item: You two should discuss '{self.user_profile.get('dream_domain')[0]}' projects!{Style.RESET_ALL}")