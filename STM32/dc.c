#include "dc.h"

void MOTOR_ON(void)
{
  HAL_GPIO_WritePin(GPIOA, IN1_PIN, GPIO_PIN_SET);   // 정방향 회전 1
  HAL_GPIO_WritePin(GPIOA, IN2_PIN, GPIO_PIN_RESET); //0
}

void MOTOR_OFF(void)
{
  HAL_GPIO_WritePin(GPIOA, IN1_PIN, GPIO_PIN_RESET); // 정지 
  HAL_GPIO_WritePin(GPIOA, IN2_PIN, GPIO_PIN_RESET);
}
