from models.sphinx import get_sphinx_client

class Searchable():
    @classmethod
    def search(cls, query, limit=10, offset=0):
        sphinx_client = get_sphinx_client()
        sphinx_client.SetLimits(offset=offset, limit=limit)
        result = sphinx_client.Query(query, cls.__tablename__)
        ids = [match['id'] for match in result['matches']]

        records = cls.query.filter(cls.id.in_(ids)).all()

        def sort(x, y):
            return y.weight - x.weight

        for record in records:
            weight = [match['weight'] for match in result['matches'] if match['id'] == record.id]
            record.weight = weight[0]

        records = sorted(records, cmp=sort)

        return dict(
            data=records,
            raw=result
        )

    @classmethod
    def count_search(cls, query):
        sphinx_client = get_sphinx_client()
        result = sphinx_client.Query(query, cls.__tablename__)
        return result['total_found']