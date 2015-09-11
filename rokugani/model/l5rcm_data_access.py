


class L5rcmDataAccess(object):

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

    def find_skill(self, skill_id):
        for i_skill in self.__dstore.skills:
            if i_skill.id == skill_id:
                return i_skill
        raise KeyError(skill_id)