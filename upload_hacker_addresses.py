import csv  # CSV 모듈 import
from app import db, app
from models import SuspiciousAddress
from datetime import datetime

def upload_hacker_addresses_from_csv(file_path):
    with app.app_context():
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                print(row)  # 각 행이 어떻게 생겼는지 확인하기 위해 출력

                # CSV 파일의 헤더에 맞춰 데이터를 가져옵니다
                address = row['hacker_address']
                cryptocurrency = 'BTC'  # 비트코인으로 고정
                reason = row.get('report_type', 'No reason provided')
                risk_score = 50  # 기본 위험 점수로 설정

                existing = SuspiciousAddress.query.filter_by(address=address).first()
                if not existing:
                    suspicious_address = SuspiciousAddress(
                        address=address,
                        cryptocurrency=cryptocurrency,
                        reason=reason,
                        first_seen=datetime.utcnow(),
                        last_seen=datetime.utcnow(),
                        risk_score=risk_score
                    )
                    db.session.add(suspicious_address)
                    print(f"Added address {address} to the database.")
                else:
                    print(f"Address {address} already exists in the database.")

            db.session.commit()

if __name__ == "__main__":
    file_path = 'hacker_addresses.csv'  # CSV 파일 경로
    upload_hacker_addresses_from_csv(file_path)
    print("All addresses have been processed.")