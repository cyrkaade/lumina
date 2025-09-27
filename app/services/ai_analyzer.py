import openai
import json
from typing import Dict
from app.config import settings

class AIAnalyzer:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    async def analyze_call_performance(self, transcript: str, call_duration: int) -> Dict:

        
        analysis_prompt = f"""
        Проанализируй запись разговора сотрудника колл-центра банка с клиентом на русском языке.
        Длительность звонка: {call_duration} секунд
        
        Транскрипт разговора:
        {transcript}
        
        Оцени работу сотрудника по следующим критериям (от 0 до 100 баллов каждый):

        1. Удовлетворенность клиента (customer_satisfaction_score) - оцени по тону, словам клиента
        2. Решение проблемы клиента (problem_resolution_score) - была ли решена проблема клиента
        3. Качество коммуникации (communication_score) - ясность, вежливость, профессионализм речи
        4. Профессионализм (professionalism_score) - знание продуктов, процедур, этикет

        Также определи:
        - Эмоциональное состояние клиента в конце звонка: frustrated/satisfied/neutral/angry/happy
        - Была ли решена проблема клиента: true/false
        - Ключевые проблемы, которые обсуждались (список строк)
        - Положительные аспекты работы сотрудника (список строк)
        - Области для улучшения (список строк)
        - Подробный анализ работы сотрудника (2-3 предложения)

        ВАЖНО: Отвечай ТОЛЬКО в формате JSON, без дополнительного текста:
        {{
            "customer_satisfaction_score": число_от_0_до_100,
            "problem_resolution_score": число_от_0_до_100,
            "communication_score": число_от_0_до_100,
            "professionalism_score": число_от_0_до_100,
            "customer_emotional_state": "одно_из_состояний",
            "issue_resolved": true_или_false,
            "key_issues": ["проблема1", "проблема2"],
            "positive_aspects": ["аспект1", "аспект2"],
            "improvement_areas": ["область1", "область2"],
            "detailed_analysis": "подробный анализ работы сотрудника"
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "Ты эксперт по оценке качества работы сотрудников колл-центра банка. Анализируй разговоры объективно и конструктивно. Отвечай только в формате JSON."
                    },
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            response_content = response.choices[0].message.content.strip()

            if response_content.startswith('```json'):
                response_content = response_content[7:-3]
            elif response_content.startswith('```'):
                response_content = response_content[3:-3]
            
            analysis_result = json.loads(response_content)
            
            score_fields = ['customer_satisfaction_score', 'problem_resolution_score', 
                          'communication_score', 'professionalism_score']
            
            for field in score_fields:
                if field in analysis_result:
                    analysis_result[field] = max(0, min(100, analysis_result[field]))
            
            return analysis_result
            
        except json.JSONDecodeError as e:
            raise Exception(f"AI response parsing failed: {str(e)}")
        except Exception as e:
            raise Exception(f"AI analysis failed: {str(e)}")