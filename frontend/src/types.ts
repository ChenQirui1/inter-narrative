export interface StoryRequest {
  story: string;
  action: string;
  code: string;
}

export interface Beat {
  beat: number;
  description: string;
}

export interface StoryResponse {
  story: string;
  beats: Beat[];
}
