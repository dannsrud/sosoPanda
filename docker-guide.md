# 🐳 Docker 사용 가이드

## 소개
Docker를 사용하여 Streamlit 웹 애플리케이션을 빌드하고 실행하는 방법을 단계별로 설명해보려고 해요.

## 사전 준비
- Docker 설치가 필요
  - Windows: [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
  - Mac: [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
  - Linux: 터미널에서 `sudo apt-get install docker.io`

설치 확인:
```bash
docker --version
```

## Docker 이미지 빌드

### 기본 빌드 명령어
```bash
docker build -t my-streamlit-app .
```

### 명령어 설명
- `docker build`: Docker 이미지 생성 명령어
- `-t my-streamlit-app`: 이미지 이름(태그) 지정
  - `my-streamlit-app` 대신 원하는 이름 사용 가능
- `.`: 현재 디렉토리의 Dockerfile 사용

### 빌드 과정 모니터링
- 빌드 중 진행 상황이 터미널에 표시됨
- 에러 발생 시 자세한 내용 확인 가능

## Docker 컨테이너 실행

### 기본 실행 명령어
```bash
docker run -d -p 8501:8501 my-streamlit-app
```

### 명령어 설명
- `-d`: 백그라운드 실행 (detached 모드)
- `-p 8501:8501`: 포트 매핑
  - 왼쪽: 호스트 포트
  - 오른쪽: 컨테이너 포트
- `my-streamlit-app`: 실행할 이미지 이름

### 추가 옵션
```bash
# 이름을 지정하여 실행
docker run -d -p 8501:8501 --name my-app my-streamlit-app

# 컨테이너 자동 제거 옵션 추가
docker run -d -p 8501:8501 --rm my-streamlit-app
```

## 애플리케이션 접속

### 로컬 접속
- 웹 브라우저에서 접속: `http://localhost:8501`
- 또는 `http://127.0.0.1:8501`

### 네트워크 접속
- 같은 네트워크 내 다른 컴퓨터에서 접속: `http://[호스트IP]:8501`

## 문제 해결 가이드

### 1. 포트 충돌 문제
```bash
# 다른 포트로 매핑하여 실행
docker run -d -p 8502:8501 my-streamlit-app
```

### 2. 권한 문제
```bash
# Linux/Mac에서 권한 문제 발생 시
sudo docker build -t my-streamlit-app .
sudo docker run -d -p 8501:8501 my-streamlit-app
```

### 3. 컨테이너 로그 확인
```bash
# 컨테이너 로그 확인
docker logs my-app

# 실시간 로그 확인
docker logs -f my-app
```

## Docker 명령어

### 컨테이너 관리
```bash
# 실행 중인 컨테이너 목록
docker ps

# 모든 컨테이너 목록
docker ps -a

# 컨테이너 중지
docker stop my-app

# 컨테이너 재시작
docker restart my-app

# 컨테이너 삭제
docker rm my-app
```

### 이미지 관리
```bash
# 이미지 목록 확인
docker images

# 사용하지 않는 이미지 삭제
docker image prune

# 특정 이미지 삭제
docker rmi my-streamlit-app
```

### 시스템 정리
```bash
# 미사용 컨테이너, 이미지, 네트워크 모두 정리
docker system prune
```

## 참고 자료
- [Docker 공식 문서](https://docs.docker.com/)
- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Docker Hub](https://hub.docker.com/)

## 주의
- 개발 중에는 로컬에서 직접 실행하고, 배포 시에만 Docker 사용을 권장
- 중요한 데이터는 볼륨을 사용하여 컨테이너 외부에 저장
- Docker Desktop의 GUI를 활용하면 컨테이너 관리가 더 쉬움