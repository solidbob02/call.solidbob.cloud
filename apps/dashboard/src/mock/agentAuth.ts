/** 최초 로그인 강제 비밀번호 설정. 계정 API가 오면 이 플래그만 서버 값으로 바꾼다. */
export interface MockAgentAccount {
  name: string;
  mustChangePassword: boolean;
}

const account: MockAgentAccount = {
  name: "조서희",
  mustChangePassword: true,
};

export function getMockAgentAccount(): MockAgentAccount {
  return { ...account };
}

export function completeMockPasswordSetup(): void {
  account.mustChangePassword = false;
}
