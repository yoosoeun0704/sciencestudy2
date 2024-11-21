import streamlit as st
import requests
import pandas as pd
from datetime import datetime

class FinancialAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://opendart.fss.or.kr/api"
        
    def get_corp_code(self, company_name):
        """기업 이름으로 고유번호 조회"""
        url = f"{self.base_url}/corpCode.xml"
        params = {
            'crtfc_key': self.api_key
        }
        
        response = requests.get(url, params=params)
        # 실제 구현시에는 XML 파싱 후 회사명으로 검색하여 고유번호 반환
        return response.json()['corp_code']

    def get_financial_statements(self, corp_code):
        """재무제표 데이터 조회"""
        url = f"{self.base_url}/fnlttSinglAcntAll.json"
        
        params = {
            'crtfc_key': self.api_key,
            'corp_code': corp_code,
            'bsns_year': datetime.now().year - 1,  # 직전 연도
            'reprt_code': '11011'  # 사업보고서
        }
        
        response = requests.get(url, params=params)
        return response.json()['list']

    def calculate_financial_ratios(self, financial_data):
        """주요 재무비율 계산"""
        # 필요한 재무 항목 추출
        current_assets = float(financial_data['current_assets'])
        current_liabilities = float(financial_data['current_liabilities'])
        total_liabilities = float(financial_data['total_liabilities'])
        total_equity = float(financial_data['total_equity'])
        net_income = float(financial_data['net_income'])
        
        # 재무비율 계산
        ratios = {
            '유동비율': (current_assets / current_liabilities) * 100,  # 유동자산 / 유동부채
            '부채비율': (total_liabilities / total_equity) * 100,  # 총부채 / 자기자본
            'ROE': (net_income / total_equity) * 100  # 당기순이익 / 자기자본
        }
        
        return ratios

    def evaluate_financial_health(self, ratios):
        """재무 건전성 평가"""
        evaluation = {}
        
        # 유동비율 평가 (200% 이상 양호, 150% 이상 보통, 미만 주의)
        if ratios['유동비율'] >= 200:
            evaluation['유동비율'] = '양호'
        elif ratios['유동비율'] >= 150:
            evaluation['유동비율'] = '보통'
        else:
            evaluation['유동비율'] = '주의'
            
        # 부채비율 평가 (100% 이하 양호, 200% 이하 보통, 초과 주의)
        if ratios['부채비율'] <= 100:
            evaluation['부채비율'] = '양호'
        elif ratios['부채비율'] <= 200:
            evaluation['부채비율'] = '보통'
        else:
            evaluation['부채비율'] = '주의'
            
        # ROE 평가 (15% 이상 양호, 5% 이상 보통, 미만 주의)
        if ratios['ROE'] >= 15:
            evaluation['ROE'] = '양호'
        elif ratios['ROE'] >= 5:
            evaluation['ROE'] = '보통'
        else:
            evaluation['ROE'] = '주의'
            
        return evaluation

def main():
    # 시스템 초기화
    analyzer = FinancialAnalyzer(api_key="81a8dcf254ab4b1a6032d65aabdfcc8e98adefa8")
    
    # 사용자 입력
    company_name = input("분석할 기업의 이름을 입력하세요: ")
    
    try:
        # 기업 고유번호 조회
        corp_code = analyzer.get_corp_code(company_name)
        
        # 재무제표 데이터 조회
        financial_data = analyzer.get_financial_statements(corp_code)
        
        # 재무비율 계산
        ratios = analyzer.calculate_financial_ratios(financial_data)
        
        # 재무 건전성 평가
        evaluation = analyzer.evaluate_financial_health(ratios)
        
        # 결과 출력
        print("\n=== 재무비율 분석 결과 ===")
        for ratio_name, ratio_value in ratios.items():
            print(f"{ratio_name}: {ratio_value:.2f}% ({evaluation[ratio_name]})")
            
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
