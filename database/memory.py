import MySQLdb


# Short term memory saves the current game moves
class ShortMemory:

    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host="127.0.0.1", user="tictactoe", passwd="tic", db="tictactoe")
        except:
            print("Please make sure you are running mysql server(XAMPP)!")
            exit()

    def save(self, move_obj):
        query = self.conn.cursor()
        position = int(move_obj["position"])
        board_before = move_obj["board_before"].replace(' ', '-')
        board_after = move_obj["board_after"].replace(' ', '-')

        if move_obj["new"]:
            move_obj["longterm_id"] = 0
        if "shortterm_id" in move_obj:
            if move_obj["shortterm_id"]:
                return move_obj["shortterm_id"]

        statement = "INSERT INTO `shortterm` (`longterm_id`, `board_before`, `position`, `board_after`, `role`, `new`, `explored`, `score`) " \
                    "VALUES (%d, '%s', %d, '%s', '%s', %d, %d, %f)" \
                    % (
                        move_obj["longterm_id"],
                        board_before,
                        position,
                        board_after,
                        move_obj["role"],
                        move_obj["new"],
                        move_obj["explored"],
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

        record["shortterm_id"] = int(record["shortterm_id"])
        record["position"] = int(record["position"])
        record["score"] = float(record["score"])
        record["board_before"] = record["board_before"].replace(' ', '-')
        record["board_after"] = record["board_after"].replace(' ', '-')

        statement = "update `shortterm` SET " \
                    "`board_before` = '%s', `position` = %d, `board_after` = '%s', " \
                    "`score` = %f, `role` = '%s'" \
                    "where id = %d" \
                    % (
                        record["board_before"],
                        record["position"],
                        record["board_after"],
                        record["score"],
                        record["role"],
                        record["shortterm_id"],
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
        statement = "select id, longterm_id, board_before, position, board_after, role, new, explored, score " \
                    "from shortterm where role = '%s' order by id DESC" % role
        try:
            query.execute(statement)
            result = []
            for (shortterm_id, longterm_id, board_before, position, board_after, role, new, explored, score) in query:
                result.append({
                    "shortterm_id": shortterm_id,
                    "longterm_id": longterm_id,
                    "board_before": board_before.replace('-', ' '),
                    "position": position,
                    "board_after": board_after.replace('-', ' '),
                    "role": role,
                    "new": new,
                    "explored": explored,
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
        statement = "select id, board_before, position, board_after, role, new, explored, score from shortterm "
        if position > -1:
            statement = statement + "where board_before = '%s' and position = %d order by id DESC" \
                        % (board, position)
        else:
            statement = statement + "where board_before = '%s' order by id DESC" \
                        % (board)
        try:
            query.execute(statement)
            result = []
            for (id, board_before, position, board_after, role, new, explored, score) in query:
                result.append({
                    "shortterm_id": id,
                    "board_before": board_before.replace('-', ' '),
                    "position": position,
                    "board_after": board_after.replace('-', ' '),
                    "role": role,
                    "new": new,
                    "explored": explored,
                    "score": score
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
        self.conn = MySQLdb.connect(host="127.0.0.1", user="tictactoe", passwd="tic", db="tictactoe")

    def save(self, record):
        query = self.conn.cursor()
        record["position"] = int(record["position"])
        record["score"] = float(record["score"])
        record["explored"] = int(record["explored"])
        record["board_before"] = record["board_before"].replace(' ', '-')
        statement = "INSERT INTO `longterm` (`board_before`, `position`, `score`, `role`, `explored`) " \
                    "VALUES ('%s', %d, %f, '%s', %d)" % (
                        record["board_before"],
                        record["position"],
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
        statement = "select id, board_before, position, score, role, explored from longterm " \
                    "where role = '%s' order by id DESC" % role
        try:
            query.execute(statement)
            result = []
            for (id, board_before, position, score, role, explored) in query:
                result.append({
                    "longterm_id": id,
                    "board_before": board_before,
                    "position": position,
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
        statement = "select id, board_before, position, score, role, explored from longterm "
        if position > -1:
            statement = statement + "where board_before = '%s' and position = %d order by id DESC" \
                        % (board, position)
        else:
            statement = statement + "where board_before = '%s' order by id DESC" \
                        % (board)
        try:
            query.execute(statement)
            result = []
            for (id, board_before, position, score, role, explored) in query:
                result.append({
                    "longterm_id": id,
                    "board_before": board_before.replace('-', ' '),
                    "position": position,
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
        if "longterm_id" not in record:
            print("longterm_id is missing in LongMemory update function!")
            raise Exception
        record["longterm_id"] = int(record["longterm_id"])
        record["position"] = int(record["position"])
        record["score"] = float(record["score"])
        record["explored"] = int(record["explored"])
        record["board_before"] = record["board_before"].replace(' ', '-')
        statement = "update `longterm` SET " \
                    "`board_before` = '%s', `position` = '%d', " \
                    "`score` = '%f', `role` = '%s', `explored` = '%d' " \
                    "where id = '%d'" \
                    % (
                        record["board_before"],
                        record["position"],
                        record["score"],
                        record["role"],
                        record["explored"],
                        record["longterm_id"],
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

    def is_next_move_explored(self, move):
        query = self.conn.cursor()
        board = move["board_before"].replace(' ', '-')
        board = list(board)
        board[move["position"]] = move["role"][0]
        if move["role"][0] == "X":
            opp_role = "O"
        else:
            opp_role = "X"

        tmpboard = "".join(board)
        result = []
        tmp = 0
        for i in range(0, len(tmpboard)):
            index = tmpboard.find('-', tmp)
            if index > -1:
                result.append(index)
                tmp = index + 1
            else:
                break
        if len(result):
            generated_boards = []
            for position in result:
                board[position] = opp_role
                generated_boards.append("".join(board))
                board[position] = '-'

            statement = "select `score`, `explored` from longterm where "

            for i in range(0, len(generated_boards) - 1):
                statement += "board_before = '%s' or " % generated_boards[i]
            else:
                statement += "board_before = '%s'" % generated_boards[-1]

            try:
                query.execute(statement)
                totalscore = 0
                for (score, explored) in query:
                    if not explored:
                        return False
                    else:
                        totalscore += score
                else:
                    number_poss = (len(result) * (len(result) -1))
                    if query.rowcount == number_poss:
                        return totalscore / number_poss
                    else:
                        return False

            except self.conn.Error as e:
                print("Error code:", e.args[0])  # error number
                print("Error message:", e.args[1])  # error message
                print("Class:", "LongMemory")  # class name
                print("Function:", "read_select")  # function name
                return False
            except:
                print("Long memory Unknown Error!")
                return False
        else:
            return True


class History:
    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="tictactoe", passwd="tic", db="tictactoe")

    def save(self, moves, result, role):
        query = self.conn.cursor()
        statement = "INSERT INTO `games_history` (`result`, `role`) value " \
                    "('%s', '%s')" % (
                        result,
                        role
                    )
        query.execute(statement)
        self.conn.commit()
        game_id = query.lastrowid

        for record in moves:
            record["position"] = int(record["position"])
            record["score"] = float(record["score"])
            record["explored"] = int(record["explored"])
            record["board_before"] = record["board_before"].replace(' ', '-')
            record["board_after"] = record["board_after"].replace(' ', '-')
            statement = "INSERT INTO `moves_history` (`game_id`, `board_before`, `position`, `board_after`, `new`, `explored`, `score`, `role`) " \
                        "VALUES ( %d, '%s', %d, '%s', '%d', '%d', %f, '%s')" % (
                            game_id,
                            record["board_before"],
                            record["position"],
                            record["board_after"],
                            record["new"],
                            record["explored"],
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

    def erase_memory(self, role=False):
        query = self.conn.cursor()
        if not role:
            role = "%"
        elif not role == "X" and not role == "O":
            return False

        statement = "DELETE FROM `shortterm` where role like '%s'" % role
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
