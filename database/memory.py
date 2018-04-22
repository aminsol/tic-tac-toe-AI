import MySQLdb


# Short term memory saves the current game moves
class ShortMemory:

    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="tictactoe")
        except:
            print("Please make sure you are running Mysql server(XAMPP)!")
            exit()

    def save(self, move_obj):
        query = self.conn.cursor()
        position = int(move_obj["position"])
        board_before = move_obj["board_before"].replace(' ', '-')
        board_after = move_obj["board_after"].replace(' ', '-')

        statement = "INSERT INTO `shortterm` (`board_before`, `position`, `board_after`, `role`, `new`, `score`) " \
                    "VALUES ('%s', %d, '%s', '%s', %d, %d)" \
                    % (
                        board_before,
                        position,
                        board_after,
                        move_obj["role"],
                        move_obj["new"],
                        move_obj["score"]
                    )
        try:
            query.execute(statement)
            self.conn.commit()
            return query.lastrowid
        except self.conn.Error as e:
            print("Error code:", e.args[0])  # error number
            print("Error message:", e.args[1])  # error message
            print("Please erase short memory after each game!")  # Guessing what might be wrong
            print("Class:", "ShortMemory")  # class name
            print("Function:", "save")  # function name
            return False
        except:
            print("Short memory Unknown Error!")
            return False

    def update(self, record):
        query = self.conn.cursor()

        record["id"] = int(record["id"])
        record["position"] = int(record["position"])
        record["score"] = int(record["score"])
        record["board_before"] = record["board_before"].replace(' ', '-')
        record["board_after"] = record["board_after"].replace(' ', '-')
        print("ok")
        statement = "update `shortterm` SET " \
                    "`board_before` = '%s', `position` = %d, `board_after` = '%s', " \
                    "`score` = %d, `role` = '%s'" \
                    "where id = %d" \
                    % (
                        record["board_before"],
                        record["position"],
                        record["board_after"],
                        record["score"],
                        record["role"],
                        record["id"],
                    )

        try:
            query.execute(statement)
            self.conn.commit()
            return True
        except self.conn.Error as e:
            print("Error code:", e.args[0])  # error number
            print("Error message:", e.args[1])  # error message
            print("Class:", "ShortMemory")  # class name
            print("Function:", "update")  # function name
            return False
        except:
            print("Short memory Unknown Error!")
            return False

    # read_all Read the entire short memory
    def read_all(self, role):
        query = self.conn.cursor()
        statement = "select id, board_before, position, board_after, role, new, score from shortterm " \
                    "where role = '%s' order by id DESC" % role
        try:
            query.execute(statement)
            result = []
            for (id, board_before, position, board_after, role, new, score) in query:
                result.append({
                    "id": id,
                    "board_before": board_before,
                    "position": position,
                    "board_after": board_after,
                    "role": role,
                    "new": new,
                    "explored": False,
                    "score": score
                })
            return result
        except self.conn.Error as e:
            print("Error code:", e.args[0])  # error number
            print("Error message:", e.args[1])  # error message
            print("Class:", "ShortMemory")  # class name
            print("Function:", "read_all")  # function name
            return False
        except:
            print("Short memory Unknown Error!")
            return False

    # Find a row based on the given board content. It return a single row.
    def read_select(self, board, position=-1):
        query = self.conn.cursor()
        board = board.replace(' ', '-')
        statement = "select id, board_before, position, board_after, role, new from shortterm "
        if position > -1:
            statement = statement + "where board_before = '%s' and position = %d order by id DESC" \
                        % (board, position)
        else:
            statement = statement + "where board_before = '%s' order by id DESC" \
                        % (board)
        try:
            query.execute(statement)
            result = []
            for (id, board_before, position, board_after, role, new) in query:
                result.append({
                    "id": id,
                    "board_before": board_before.replace('-', ' '),
                    "position": position,
                    "board_after": board_after.replace('-', ' '),
                    "role": role,
                    "new": new
                })
            return result
        except self.conn.Error as e:
            print("Error code:", e.args[0])  # error number
            print("Error message:", e.args[1])  # error message
            print("Class:", "ShortMemory")  # class name
            print("Function:", "read_select")  # function name
            return False
        except:
            print("Short memory Unknown Error!")
            return False

    def new_moves(self, role):
        query = self.conn.cursor()
        statement = "select id, board_before, position, board_after, role, new from shortterm " \
                    "where role = %s and new = TRUE " % role
        try:
            query.execute(statement)
            result = []
            for (id, board_before, position, board_after, role, new) in query:
                result.append({
                    "id": id,
                    "board_before": board_before.replace('-', ' '),
                    "position": position,
                    "board_after": board_after.replace('-', ' '),
                    "role": role,
                    "new": new
                })
            return result
        except self.conn.Error as e:
            print("Error code:", e.args[0])  # error number
            print("Error message:", e.args[1])  # error message
            print("Class:", "ShortMemory")  # class name
            print("Function:", "new_moves")  # function name
            return False
        except:
            print("Short memory Unknown Error!")
            return False

    # Erases shortterm table


# The main difference between short and long term is that short term memory must be erased after each game.
# Long term memory contain score of previous position but short term memory does not
class LongMemory:

    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="tictactoe")

    def save(self, record):
        query = self.conn.cursor()
        record["position"] = int(record["position"])
        record["score"] = int(record["score"])
        record["explored"] = int(record["explored"])
        record["board_before"] = record["board_before"].replace(' ', '-')
        record["board_after"] = record["board_after"].replace(' ', '-')
        statement = "INSERT INTO `longterm` (`board_before`, `position`, `board_after`, `score`, `role`, `explored`) " \
                    "VALUES ('%s', %d, '%s', %d, '%s', %d)" % (
                        record["board_before"],
                        record["position"],
                        record["board_after"],
                        record["score"],
                        record["role"],
                        record["explored"]
                    )
        try:
            query.execute(statement)
            self.conn.commit()
            return True
        except self.conn.Error as e:
            print("Error code:", e.args[0])  # error number
            print("Error message:", e.args[1])  # error message
            print(
                "Only new position are allowed You can update existing moves through update method!")  # Guessing what might be wrong

            print("Class:", "LongMemory")  # class name
            print("Function:", "save")  # function name
            return False
        except:
            print("Long memory Unknown Error!")
            return False

    def read_all(self, role):
        query = self.conn.cursor()
        statement = "select id, board_before, position, board_after, score, role, explored from longterm " \
                    "where role = '%s' order by id DESC" % role
        try:
            query.execute(statement)
            result = []
            for (id, board_before, position, board_after, score, role, explored) in query:
                result.append({
                    "id": id,
                    "board_before": board_before,
                    "position": position,
                    "board_after": board_after,
                    "score": score,
                    "role": role,
                    "explored": explored
                })
            return result
        except self.conn.Error as e:
            print("Error code:", e.args[0])  # error number
            print("Error message:", e.args[1])  # error message
            print("Class:", "LongMemory")  # class name
            print("Function:", "read_all")  # function name
            return False
        except:
            print("Long memory Unknown Error!")
            return False

    # read_select only return the row with specified board content.
    # This function can be used to find a specific position if position parameter is set
    def read_select(self, board, position=-1):
        query = self.conn.cursor()
        board = board.replace(' ', '-')
        statement = "select id, board_before, position, board_after, score, role, explored from longterm "
        if position > -1:
            statement = statement + "where board_before = '%s' and position = %d order by id DESC" \
                        % (board, position)
        else:
            statement = statement + "where board_before = '%s' order by id DESC" \
                        % (board)
        try:
            query.execute(statement)
            result = []
            for (id, board_before, position, board_after, score, role, explored) in query:
                result.append({
                    "id": id,
                    "board_before": board_before.replace('-', ' '),
                    "position": position,
                    "board_after": board_after.replace('-', ' '),
                    "score": score,
                    "role": role,
                    "explored": explored
                })
            return result
        except self.conn.Error as e:
            print("Error code:", e.args[0])  # error number
            print("Error message:", e.args[1])  # error message
            print("Class:", "LongMemory")  # class name
            print("Function:", "read_select")  # function name
            return False
        except:
            print("Long memory Unknown Error!")
            return False

    def update(self, record):
        query = self.conn.cursor()
        record["id"] = int(record["id"])
        record["position"] = int(record["position"])
        record["score"] = int(record["score"])
        record["explored"] = int(record["explored"])
        record["board_before"] = record["board_before"].replace(' ', '-')
        record["board_after"] = record["board_after"].replace(' ', '-')
        statement = "update `longterm` SET " \
                    "`board_before` = '%s', `position` = %d, `board_after` = '%s', " \
                    "`score` = %d, `role` = '%s', `explored` = %d " \
                    "where id = %d" \
                    % (
                        record["board_before"],
                        record["position"],
                        record["board_after"],
                        record["score"],
                        record["role"],
                        record["explored"],
                        record["id"],
                    )

        try:
            query.execute(statement)
            self.conn.commit()
            return True
        except self.conn.Error as e:
            print("Error code:", e.args[0])  # error number
            print("Error message:", e.args[1])  # error message
            print("Class:", "LongMemory")  # class name
            print("Function:", "update")  # function name
            return False
        except:
            print("Long memory Unknown Error!")
            return False


class History:
    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="tictactoe")

    def save(self, moves, result, role):
        query = self.conn.cursor()
        statement = "INSERT INTO `games_history` (`result`, `role`) value " \
                    "(%s, %s)" % (
                        result,
                        role
                    )
        query.execute(statement)
        self.conn.commit()
        game_id = query.lastrowid

        for record in moves:
            record["position"] = int(record["position"])
            record["score"] = int(record["score"])
            record["explored"] = int(record["explored"])
            record["board_before"] = record["board_before"].replace(' ', '-')
            record["board_after"] = record["board_after"].replace(' ', '-')
            statement = "INSERT INTO `moves_history` (`game_id`, `board_before`, `position`, `board_after`, `score`, `role`) " \
                        "VALUES ( %d, '%s', %d, '%s', %d, '%s')" % (
                            game_id,
                            record["board_before"],
                            record["position"],
                            record["board_after"],
                            record["score"],
                            record["role"]
                        )
            try:
                query.execute(statement)
            except self.conn.Error as e:
                print("Error code:", e.args[0])  # error number
                print("Error message:", e.args[1])  # error message
                print("Class:", "LongMemory")  # class name
                print("Function:", "update")  # function name
                return False
            except:
                print("Long memory Unknown Error!")
                return False

        self.conn.commit()
        return True

    def erase_memory(self):
        query = self.conn.cursor()
        statement = "DELETE FROM `shortterm`"
        try:
            query.execute(statement)
            self.conn.commit()
            return True
        except self.conn.Error as e:
            print("Error code:", e.args[0])  # error number
            print("Error message:", e.args[1])  # error message
            print("Class:", "ShortMemory")  # class name
            print("Function:", "erase")  # function name
            return False
        except:
            print("Short memory Unknown Error!")
            return False
