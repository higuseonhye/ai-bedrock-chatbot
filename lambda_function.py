# 🚀 Production-Ready AWS Lambda Handler
# Colab 테스트 완료 → AWS Lambda 배포 준비
# 
# ⚡ AWS Lambda 설정 (최신 버전):
# Runtime: python3.13 (최신! 2029년까지 지원)
# Architecture: x86_64 (또는 arm64 - 더 저렴함)
# Memory: 512 MB (기본값)
# Timeout: 30초

import json
import boto3
import logging
from typing import Dict, Any
from datetime import datetime

# Lambda 로깅 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ProductionAIAgent:
    """AWS Lambda에서 실행되는 Production AI Agent"""
    
    def __init__(self):
        # Lambda 환경에서는 IAM 역할을 통해 자동 인증
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        logger.info("AI Agent 초기화 완료")
    
    def generate_response(self, user_message: str, conversation_id: str = None) -> Dict[str, Any]:
        """AI 응답 생성 (Lambda 최적화)"""
        try:
            logger.info(f"메시지 처리 시작: {user_message[:50]}...")
            
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "temperature": 0.7,
                "messages": [{"role": "user", "content": user_message}]
            }
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            result = json.loads(response['body'].read())
            ai_response = result['content'][0]['text']
            
            logger.info("AI 응답 생성 성공")
            
            return {
                "success": True,
                "response": ai_response,
                "conversation_id": conversation_id,
                "timestamp": datetime.utcnow().isoformat(),
                "environment": "AWS Lambda",
                "model": self.model_id
            }
            
        except Exception as e:
            logger.error(f"AI 응답 생성 실패: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

def lambda_handler(event, context):
    """
    AWS Lambda의 메인 핸들러
    Function URL에서 호출됨
    """
    
    # CORS 헤더 설정 (브라우저 호환성 보장)
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With, Accept, Origin',
        'Access-Control-Max-Age': '86400'
    }
    
    try:
        logger.info("=== Lambda 함수 실행 시작 ===")
        logger.info(f"Event keys: {list(event.keys())}")
        logger.info(f"HTTP Method: {event.get('requestContext', {}).get('http', {}).get('method', 'UNKNOWN')}")
        
        # Function URL에서는 requestContext.http.method 사용
        http_method = event.get('requestContext', {}).get('http', {}).get('method', 'POST')
        
        # CORS preflight 요청 처리
        if http_method == 'OPTIONS':
            logger.info("CORS preflight 요청 처리")
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # POST 요청이 아닌 경우
        if http_method != 'POST':
            logger.warning(f"지원하지 않는 HTTP 메서드: {http_method}")
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': f'Method {http_method} not allowed. Use POST.'
                })
            }
        
        # 요청 body 파싱
        body_str = event.get('body', '')
        if not body_str:
            logger.error("Request body가 없습니다")
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'Request body is required'
                })
            }
        
        # JSON 파싱
        try:
            body = json.loads(body_str)
            logger.info(f"파싱된 body: {body}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {str(e)}")
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'Invalid JSON in request body'
                })
            }
        
        # 필수 필드 확인
        user_message = body.get('message', '').strip()
        if not user_message:
            logger.error("메시지가 비어있습니다")
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'success': False,
                    'error': 'Message field is required and cannot be empty'
                })
            }
        
        conversation_id = body.get('conversation_id')
        logger.info(f"메시지 처리 시작: {user_message[:100]}...")
        
        # AI Agent 실행
        agent = ProductionAIAgent()
        result = agent.generate_response(user_message, conversation_id)
        
        # 응답 생성
        status_code = 200 if result['success'] else 500
        
        logger.info(f"=== Lambda 함수 실행 완료 === Status: {status_code}")
        
        return {
            'statusCode': status_code,
            'headers': headers,
            'body': json.dumps(result, ensure_ascii=False)
        }
        
    except Exception as e:
        logger.error(f"Lambda 핸들러 오류: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': 'Internal server error',
                'timestamp': datetime.utcnow().isoformat()
            })
        }

# 로컬 테스트용 (개발 시에만 사용)
if __name__ == "__main__":
    print("🧪 로컬 테스트 모드")
    print("⚠️  실제 배포는 AWS Lambda에서 실행됩니다")
    
    # 테스트 이벤트 시뮬레이션
    test_event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'message': 'Hello from local test!',
            'conversation_id': 'test-123'
        })
    }
    
    test_context = {}
    
    print("📝 테스트 이벤트 처리 중...")
    result = lambda_handler(test_event, test_context)
    
    print(f"📊 응답 코드: {result['statusCode']}")
    print(f"📄 응답 내용: {result['body']}")
    
    print("\n" + "="*50)
    print("🚀 다음 단계:")
    print("1. AWS Lambda 함수 생성")
    print("2. API Gateway 연결") 
    print("3. 프로덕션 배포 완료!")
