from abc import ABC


class DomainModel(ABC):
    def update(self, domain_model: "DomainModel"):
        for key, value in domain_model.__dict__.items():
            if not key.startswith("_") and key is not "id":
                setattr(self, key, value)
