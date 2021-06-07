import grpc
import grpc_code.ee613_team_pb2 as pb
import grpc_code.ee613_team_pb2_grpc as pb_grpc
from concurrent import futures
import menu_class as mc

class Members():
    def __init__(self):
        # member를 dict 형태로 저장. 'id' : ['pwd', point] 
        self.members = {}
    
    def has_id(self, id_):
        return (id_ in self.members)
    
    def current_point(self, id_):
        return self.members[id_][1]

    def recharge_point(self, id_, rp):
        self.members[id_][1] += rp
        return self.members[id_][1]
    
    def login_(self, id_, pwd_):
        if self.members[id_][0] == pwd_:
            return True
        else:
            return False
    
    def signup(self, id_, pwd_, point_=0):
        if self.has_id(id_):
            return False
        else:
            self.members[id_] = [pwd_, point_]
            return True

class ee613_server(pb_grpc.EE613_Team_PServicer):
    def __init__(self):
        super().__init__()
        self.member_class = Members()

    # Login_ success or fail + menu
    def Login_(self, request, context):
        if self.member_class.has_id(request.u_id):
            print("ID found")
            if self.member_class.login_(request.u_id, request.u_pwd):
                menu_info = []
                # read mc, and then keep sending the menu info
                for menu_id in mc.menu_class:
                    menu_info.append(pb.Food_Info(menu_id=menu_id, menu_name=mc.menu_class[menu_id][0], menu_price=mc.menu_class[menu_id][1], menu_num=mc.menu_class[menu_id][2]))
                response = pb.Login_Respond(login_success=True, fd_info=menu_info)
                print("Login Success")

            else:
                response = pb.Login_Respond(login_success=False)
        else:
            response = pb.Login_Respond(login_success=False)
        return response
    
    def Signin(self, request, context):
        if self.member_class.signup(request.u_id, request.u_pwd):
            response = pb.Signin_Respond(signin_success=True)
        else:
            response = pb.Signin_Respond(signin_success=False)
        print(self.member_class.members)
        return response
    
    def Order_Food(self, request, context):
        istrue_ = True
        tc = 0
        # first, check the order info - > request.orders
        for order in request.orders_:
            if mc.menu_class[order.menu_id][2] < order.menu_num:
                istrue_= False
                break
        # check whether the total cost is right
        if istrue_:
            for order in request.orders_:
                tc += mc.menu_class[order.menu_id][1] * order.menu_num
            if tc != request.total_cost:
                istrue_ = False
        # check the remaining points
        if istrue_:
            if self.member_class.current_point(request.uif.u_id) >= tc:
                self.member_class.members[request.uif.u_id][1] -= tc
            else:
                istrue_ = False
        if istrue_:
            for order in request.orders_:
                mc.menu_class[order.menu_id][2] -= order.menu_num
        response=pb.Order_Respond(istrue=istrue_,remaining_points=self.member_class.current_point(request.uif.u_id))
        return response

    def Point_Check(self, request, context):
        response = pb.Remaining_Points(remaining_points=self.member_class.current_point(request.u_id))
        return response

    def Point_Recharge(self, request, context):
        response = pb.Remaining_Points(remaining_points=self.member_class.recharge_point(request.uif.u_id,  request.recharging_points))
        return response

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor())
    pb_grpc.add_EE613_Team_PServicer_to_server(ee613_server(), server)
    server.add_insecure_port('localhost:9999')
    server.start()
    server.wait_for_termination()