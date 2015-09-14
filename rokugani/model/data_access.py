


class DataAccess(object):

    def __init__(self, packs_dir):
        import dal
        self._locations = [packs_dir]
        self.__dstore = dal.Data(self._locations)

    @property
    def clans(self):
        return self.__dstore.clans

    @property
    def families(self):
        return self.__dstore.families

    @property
    def schools(self):
        return self.__dstore.schools

    @property
    def skills(self):
        return self.__dstore.skills

    @property
    def merits(self):
        return self.__dstore.merits

    @property
    def flaws(self):
        return self.__dstore.flaws

    @property
    def traits(self):
        return self.__dstore.traits

    @property
    def rings(self):
        return self.__dstore.rings

    def find_skill(self, skill_id):
        for i_skill in self.__dstore.skills:
            if i_skill.id == skill_id:
                return i_skill
        raise KeyError(skill_id)

    def find_merit(self, merit_id):
        for i_merit in self.__dstore.merits:
            if i_merit.id == merit_id:
                return i_merit
        raise KeyError(merit_id)

    def find_flaw(self, flaw_id):
        for i_flaw in self.__dstore.flaws:
            if i_flaw.id == flaw_id:
                return i_flaw
        raise KeyError(flaw_id)
