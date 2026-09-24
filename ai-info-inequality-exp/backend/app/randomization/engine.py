import random
from sqlalchemy.orm import Session
from app.db.models import Participant, AILiteracy, RandomizationAllocation, LanguageBackground, ScreeningLog, ConsentLog
from app.config import frozen_config

class RandomizationEngine:
    ARMS = ["ENGLISH_ONLY", "HINDI_ONLY", "CODE_SWITCHING"]

    def __init__(self, db: Session):
        self.db = db

    def get_stratum(self, ails_score: int) -> str:
        threshold = frozen_config["randomization"]["strata_cutoffs"]["median_split_threshold"]
        if ails_score < threshold:
            return "LOW"
        return "HIGH"

    def verify_eligibility_for_randomization(self, participant_id: str) -> tuple[bool, str]:
        participant = self.db.query(Participant).filter(Participant.participant_id == participant_id).first()
        if not participant:
            return False, "Participant not found."

        if not participant.consent_log or not participant.consent_log.agreed_to_terms:
            return False, "Consent not provided."

        if not participant.screening_log or not participant.screening_log.passed:
            return False, "Bilingual screening not passed."

        if not participant.language_bg:
            return False, "Language background questionnaire not completed."

        if not participant.ai_literacy:
            return False, "AI Literacy Scale not completed."

        if participant.randomization:
            return False, "Participant already randomized."

        return True, "Eligible"

    def allocate_participant(self, participant_id: str) -> RandomizationAllocation:
        is_eligible, msg = self.verify_eligibility_for_randomization(participant_id)
        if not is_eligible:
            raise ValueError(f"Cannot randomize participant {participant_id}: {msg}")

        ai_lit = self.db.query(AILiteracy).filter(AILiteracy.participant_id == participant_id).first()
        stratum = self.get_stratum(ai_lit.total_score)

        # Get existing allocations for this stratum
        existing_allocations = (
            self.db.query(RandomizationAllocation)
            .filter(RandomizationAllocation.stratum == stratum)
            .order_by(RandomizationAllocation.alloc_id.asc())
            .all()
        )

        # Check if current block has space
        if existing_allocations:
            last_alloc = existing_allocations[-1]
            last_block_id = last_alloc.block_id
            block_items = [a for a in existing_allocations if a.block_id == last_block_id]
            block_size = last_alloc.block_size

            if len(block_items) < block_size:
                # Find which arms are remaining in this block sequence
                used_arms = [a.assigned_arm for a in block_items]
                
                # Re-construct original block assignment sequence
                # For reproducibility, we generate the block sequence using block_id as seed
                rng = random.Random(f"{stratum}_{last_block_id}")
                
                if block_size == 3:
                    full_block = list(self.ARMS)
                    rng.shuffle(full_block)
                else: # size 6
                    full_block = list(self.ARMS) + list(self.ARMS)
                    rng.shuffle(full_block)

                assigned_arm = full_block[len(used_arms)]
                
                new_allocation = RandomizationAllocation(
                    participant_id=participant_id,
                    stratum=stratum,
                    block_id=last_block_id,
                    block_size=block_size,
                    assigned_arm=assigned_arm
                )
                self.db.add(new_allocation)
                
                # Update participant status
                participant = self.db.query(Participant).filter(Participant.participant_id == participant_id).first()
                participant.status = "RANDOMIZED"
                
                self.db.commit()
                self.db.refresh(new_allocation)
                return new_allocation

        # Start new block
        new_block_id = (max([a.block_id for a in existing_allocations], default=0)) + 1
        new_block_size = random.choice([3, 6])
        
        rng = random.Random(f"{stratum}_{new_block_id}")
        if new_block_size == 3:
            full_block = list(self.ARMS)
            rng.shuffle(full_block)
        else:
            full_block = list(self.ARMS) + list(self.ARMS)
            rng.shuffle(full_block)

        assigned_arm = full_block[0]

        new_allocation = RandomizationAllocation(
            participant_id=participant_id,
            stratum=stratum,
            block_id=new_block_id,
            block_size=new_block_size,
            assigned_arm=assigned_arm
        )
        self.db.add(new_allocation)
        
        participant = self.db.query(Participant).filter(Participant.participant_id == participant_id).first()
        participant.status = "RANDOMIZED"
        
        self.db.commit()
        self.db.refresh(new_allocation)
        return new_allocation
