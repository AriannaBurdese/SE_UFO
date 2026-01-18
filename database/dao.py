from database.DB_connect import DBConnect
from model.sighting import Sighting
from model.state import State
from model.neighbor import Neighbor


class DAO:
    @staticmethod
    def get_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT *
                    FROM state
                    """)
        try:
            cursor.execute(query)
            for row in cursor:
                stato = State(**row)

                result.append(stato)

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_weighted_neighbors(year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ( """SELECT n.state1 AS s1, n.state2 AS s2, COUNT(*) AS N
                    FROM neighbor n
                    INNER JOIN sighting s ON (s.state = n.state1 OR s.state = n.state2)
                    WHERE YEAR(s.s_datetime) = %s AND s.shape = %s
                    GROUP BY n.state1, n.state2""")

        try:
            cursor.execute(query, (year, shape))
            for row in cursor:
                neighbor = (row["s1"],row["s2"], row["N"])
                result.append((neighbor))

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_sighting():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT *
                    FROM sighting s
                    ORDER BY s_datetime ASC""") # lista ordinata di anni
                  

        try:
            cursor.execute(query)
            for row in cursor:
                sighting = Sighting(**row)

                result.append(sighting)

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT DISTINCT s.shape
                    FROM sighting s
                    WHERE shape <> '' AND YEAR(s_datetime) = %s
                                    """)
        try:
            cursor.execute(query, (year,))
            for row in cursor:
                forma = (row["shape"])

                result.append(forma)

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result



"""SELECT LEAST(n.state1, n.state2) AS s1, GREATEST(n.state1, n.state2) AS s2,
                        #COUNT(*) AS N
                    FROM sighting s, neighbor n
                    WHERE year(s.s_datetime) = %s
                        AND s.shape = %s
                        AND (s.state = n.state1 OR s.state = n.state2)
                    GROUP BY s1, s2"""



"""SELECT n.state1 AS s1, n.state2 AS s2, COUNT(*) AS N
                    FROM neighbor n
                    INNER JOIN sighting s ON (s.state = n.state1 OR s.state = n.state2)
                    WHERE YEAR(s.s_datetime) = %s AND s.shape = %s
                    GROUP BY n.state1, n.state2"""

