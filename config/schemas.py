from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Championship(Base):
    __tablename__ = "championship_infos"
    # Clé primaire
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Informations temporelles
    date_text: Mapped[Optional[str]]
    unix_timestamp: Mapped[Optional[str]]
    day: Mapped[str]
    
    # Identifiants
    match_id: Mapped[int] = mapped_column(int, unique=True)
    coupe_id: Mapped[Optional[int]] = mapped_column('id_coupe', int, nullable=True)

    # Équipe A
    team_a_logo_url: Mapped[Optional[str]]
    team_a_name: Mapped[Optional[str]]
    team_a_short: Mapped[Optional[str]]
    team_a_goal: Mapped[Optional[str]]
    team_a_shots_on_target: Mapped[Optional[str]]
    team_a_possession: Mapped[Optional[str]]
    team_a_passes: Mapped[Optional[str]]
    team_a_pass_accuracy: Mapped[Optional[str]]
    team_a_fouls: Mapped[Optional[str]]
    team_a_yellow_cards: Mapped[Optional[str]]
    team_a_red_cards: Mapped[Optional[str]]
    team_a_offsides: Mapped[Optional[str]]
    team_a_corners: Mapped[Optional[str]]
    team_a_goal_times: Mapped[Optional[str]]

    # Équipe B
    team_b_logo_url: Mapped[Optional[str]]
    team_b_name: Mapped[Optional[str]]
    team_b_short: Mapped[Optional[str]]
    team_b_goal: Mapped[Optional[str]]
    team_b_shots_on_target: Mapped[Optional[str]]
    team_b_possession: Mapped[Optional[str]] 
    team_b_passes: Mapped[Optional[str]]
    team_b_pass_accuracy: Mapped[Optional[str]]
    team_b_fouls: Mapped[Optional[str]]
    team_b_yellow_cards: Mapped[Optional[str]]
    team_b_red_cards: Mapped[Optional[str]]
    team_b_offsides: Mapped[Optional[str]]
    team_b_corners: Mapped[Optional[str]]
    team_b_goal_times: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return (
            f"EuroMatch(id={self.id!r}, "
            f"match_id={self.match_id!r}, "
            f"{self.team_a_name!r} {self.team_a_goal}-{self.team_b_goal} {self.team_b_name!r}, "
            f"date={self.date_text!r})"
        )
    
class Team(Base):
    __tablename__ = "team_infos"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    players: Mapped[list["Player"]] = relationship(back_populates="team", cascade="all, delete-orphan")
    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, name={self.name!r}, players={self.players!r})"

class Player(Base):
    __tablename__ = "player_infos"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    team_id: Mapped[int] = mapped_column(ForeignKey("team_infos.id"))
    team: Mapped["Team"] = relationship(back_populates="players")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"