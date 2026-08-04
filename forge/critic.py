"""Evaluate explicit artwork evidence against Studio canon."""

from __future__ import annotations

from collections.abc import Mapping

from forge.critic_model import ArtworkEvidence, Critique
from forge.critic_rules import (
    advisory_findings,
    check_camera,
    check_continuity,
    check_immutable_elements,
    check_readable_text,
    check_required_objects,
)
from forge.object_model import StudioObject
from forge.objects import OBJECTS_BY_ID
from forge.world import World
from forge.worlds import WORLDS_BY_KEY


class StudioCritic:
    """A humble canon reviewer that never approves or rejects artwork."""

    def __init__(
        self,
        worlds_by_key: Mapping[str, World] = WORLDS_BY_KEY,
        objects_by_id: Mapping[str, StudioObject] = OBJECTS_BY_ID,
    ) -> None:
        self._worlds_by_key = worlds_by_key
        self._objects_by_id = objects_by_id

    def evaluate(self, evidence: ArtworkEvidence) -> Critique:
        if not isinstance(evidence, ArtworkEvidence):
            raise ValueError("evidence must be ArtworkEvidence")

        world = self._worlds_by_key.get(evidence.world_key)
        if world is None:
            raise ValueError(f"unknown world key: {evidence.world_key}")

        referenced_ids = {
            *evidence.present_object_ids,
            *evidence.absent_object_ids,
            *(claim.object_id for claim in evidence.continuity_claims),
        }
        unknown_ids = sorted(referenced_ids - self._objects_by_id.keys())
        if unknown_ids:
            raise ValueError(f"unknown object ID: {unknown_ids[0]}")

        unknown_worlds = sorted(
            {
                claim.prior_world_key
                for claim in evidence.continuity_claims
                if claim.prior_world_key not in self._worlds_by_key
            }
        )
        if unknown_worlds:
            raise ValueError(f"unknown world key: {unknown_worlds[0]}")

        findings = (
            *check_camera(evidence, world),
            *check_required_objects(evidence, world),
            *check_immutable_elements(evidence, world),
            *check_readable_text(evidence, world),
            *check_continuity(evidence, world, self._objects_by_id),
            *advisory_findings(evidence, world),
        )
        return Critique(world=world, findings=findings)
