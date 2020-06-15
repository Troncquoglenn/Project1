from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    
    # sensor methods
    @staticmethod
    def read_sensor():
        sql = "SELECT * from Sensor"
        return Database.get_rows(sql)
    
    @staticmethod
    def update_sensor(id, waarde):
        sql = "UPDATE sensor SET waarde = %s WHERE sensorid = %s"
        params = [waarde, id]
        return Database.execute_sql(sql, params)

    # meting methods
    @staticmethod
    def read_meting(id):
        sql = "SELECT metingid, DATE_FORMAT(meetdatum, '%Y:%c:%d-%H:%i:%S') as meetdatum, meetwaarde FROM meting WHERE sensorid = %s"
        params = [id]
        return Database.get_rows(sql, params)

    @staticmethod
    def update_meting(datum, waarde, id):
        sql = "INSERT INTO meting(meetdatum, meetwaarde, actuatorid, sensorid) VALUES(%s, %s, 1, %s)"
        params = [datum, waarde, id]
        return Database.execute_sql(sql, params)

    




    @staticmethod
    def read_status_lamp_by_id(id):
        sql = "SELECT * from lampen WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE metingen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)