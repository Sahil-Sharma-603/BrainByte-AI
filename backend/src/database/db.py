# Helper function interacting with the database Models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models

def get_challenge_quota(db: Session, user_id: str):
    return (db.query(models.ChallengeQuota).filter(models.ChallengeQuota.user_id == user_id).first())
    


def create_challenge_quota(db: Session, user_id: str): 
  db_quota = models.ChallengeQuota(user_id= user_id)
  db.add(db_quota)
  db.commit()
  db.refresh(db_quota)
  return db_quota


def reset_quota_if_needed(db: Session, quota: models.ChallengeQuota):
    if quota.last_reset_date.date() < datetime.utcnow().date():
        quota.quota_remaining = 50  # Reset to default quota
        quota.last_reset_date = datetime.utcnow()
        db.commit()
        db.refresh(quota)
    return quota


