import qi

IP_NAO = "http://localhost:9000"
PORT_NAO = "9449"


def apply_to_robot_nao(names_times_keys_instance, ip = IP_NAO, port = PORT_NAO):
    app = qi.Session()
    app.connect("tcp://{}:{}".format(ip, port))

    #self.postureProxy = self.app.service("ALRobotPosture")
    motionProxy = app.service("ALMotion")
    motionProxy.angleInterpolationBezier(
        names_times_keys_instance.names,
        names_times_keys_instance.times,
        names_times_keys_instance.keys)
g.apply_to_robot_nao = apply_to_robot_nao