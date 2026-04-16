# Week 7 실습 기록

## 목표
가시 오브젝트 구현, 피격 시 화면 흔들림 구현

## AI 대화 기록

**Q1: 바닥에서 !표시가 나오고 레이저와 동일하게 일정 시간 후 가시가 나오도록 코드를 수정

- AI 답변: spikes 변수 추가 후 spikes.append()로 생성하고 if invincible==0 and hitbox.colliderect):로 충돌 처리하여 가시 구현

**Q2: 피격 시 화면 흔들림 구현

- AI 답변: 피격 시 shake_timer shake_intensity 설정하고 매 프레임 offset_x=random.randint(), offset_y=random.randint() 계산 후 screen.blit()처럼 모든 그리기 좌표에 더해 화면 흔들림 구현

**Q3: 플레이어 애니메이션이 좌우 이동할 때 좌우 반전되독록 수정

- AI 답변: 방향 변수로 좌우를 판단해 왼쪽일 때만 pygame.transform.flip() 적용
