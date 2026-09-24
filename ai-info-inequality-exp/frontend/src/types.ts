export type ExperimentalArm = 'ENGLISH_ONLY' | 'HINDI_ONLY' | 'CODE_SWITCHING';

export type SessionStatus = 
  | 'CONSENTED' 
  | 'SCREENED' 
  | 'BASELINE_DONE' 
  | 'RANDOMIZED' 
  | 'IN_PROGRESS' 
  | 'COMPLETED' 
  | 'EXCLUDED';

export interface TaskState {
  task_id: 'PMEGP' | 'PM_VISHWAKARMA' | 'PM_SVANIDHI';
  position: number;
  status: 'STARTED' | 'COMPLETED' | 'PENDING' | 'TIMED_OUT';
}

export interface ScenarioDetails {
  task_id: string;
  name: string;
  domain: string;
  persona: {
    name: string;
    age: number;
    gender: string;
    social_category?: string;
    location: string;
    proposed_project?: string;
    trade?: string;
    vending_activity?: string;
    background_summary: string;
  };
  official_sources: Array<{ title: string; url: string }>;
}

export interface ChatMessage {
  id?: number;
  sender: 'USER' | 'AI';
  text: string;
  timestamp: string;
}
