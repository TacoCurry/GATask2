# GATask2
This program assigns h/w resources for a task using GA to optimize power 

## Input
자세한 내용은 파일 내부의 설명을 참고하세요.
- input_configuration.txt: 메모리, 프로세서, GA 정보 
- input_tasks.txt: 실시간 태스크 정보 

## Run
정보를 위 input 파일에 형식을 맞추어 입력하고, Main.py를 실행한다.<br>

## Output
ceil(util)부터 코어의 개수에 대한 GA 결과가 각각 출력된다.
최종 솔루션셋의 솔루션 중 가장 전력 소모량이 적은 솔루션이 result.txt로 출력된다.
각 줄마다 input_tasks의 task에 하나씩 대응하며, 프로세서의 voltage/frequency 모드와 메모리 종류 순으로 출력된다.

## Demo
GA Demo: 10000세대 진화 결과
https://youtu.be/aSAMVM6kDyg
