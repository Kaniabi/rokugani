


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
        return self._find_by_id(self.__dstore.skills, skill_id)

    def find_merit(self, merit_id):
        return self._find_by_id(self.__dstore.merits, merit_id)

    def find_flaw(self, flaw_id):
        return self._find_by_id(self.__dstore.flaws, flaw_id)

    def find_school(self, school_id):
        return self._find_by_id(self.__dstore.schools, school_id)

    def _find_by_id(self, iter, id):
        for i in iter:
            if i.id == id:
                return i
        raise KeyError(id)
