from numpy import sin, cos, pi
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

g = 9.80665

class Object:
    def __init__(self, mass: float, length: float, angle: float,
                    angle_: float = 0, angle__: float = 0):
        self.mass = mass
        self.length = length
        self.angle = angle
        self.angle_ = angle_
        self.angle__ = angle__

    @property
    def xy(self):
        return self.length * sin(self.angle), self.length * cos(self.angle)

    def __add__(self, other):
        (x1, y1), (x2, y2) = self.xy, other.xy
        return x1 + x2, y1 + y2

class Pendulum:
    def __init__(self, object1: Object, object2: Object,
                    dt: float = 0.02):
        self.o1 = object1
        self.o2 = object2
        self.dt = dt

        self.fig = plt.figure()
        L = object1.length + object2.length
        self.ax = self.fig.add_subplot(autoscale_on = False,
                    xlim = (-L, L), ylim = (L, -L))
        self.ax.set_aspect("equal")
        self.ax.grid()

        self.line, = self.ax.plot([], [], 'o-', lw = 2)
        self.trace, = self.ax.plot([], [], '.-',lw = 1, ms = 2)
        self.time_template = 'time = %.1fs'
        self.time_text = self.ax.text(0.05, 0.9, '', transform = self.ax.transAxes)
        self.trace_x, self.trace_y = deque(maxlen = 500), deque(maxlen = 500)

    def calculate_xy(self):
        o1, o2 = self.o1, self.o2

        # update angle__
        num  = -g * (2 * o1.mass + o2.mass) * sin(o1.angle)
        num += -o2.mass * g * sin(o1.angle - 2 * o2.angle)
        num += -2 * sin(o1.angle - o2.angle) * o2.mass * \
               (o2.angle_**2 * o2.length + o1.angle_**2 * o1.length * cos(o1.angle - o2.angle))
        denum = o1.length * (2 * o1.mass + o2.mass - o2.mass * \
                cos(2 * o1.angle - 2 * o2.angle))
        o1.angle__ = num/denum

        num  = o1.angle_**2 * o1.length * (o1.mass + o2.mass);
        num += g * (o1.mass + o2.mass) * cos(o1.angle);
        num += o2.angle_**2 * o2.length * o2.mass * cos(o1.angle - o2.angle);
        denum = o2.length * (2 * o1.mass + o2.mass - o2.mass * \
                cos(2 * o1.angle - 2 * o2.angle));
        o2.angle__ = 2 * sin(o1.angle - o2.angle) * num/denum;

        # update angle_
        o1.angle_ += o1.angle__ * self.dt;
        o2.angle_ += o2.angle__ * self.dt;

        # update angle
        o1.angle += o1.angle_ * self.dt;
        o2.angle += o2.angle_ * self.dt;

        # calculate xy
        return o1.xy, o1+o2

    def animate_func(self, i):
        (x1, y1), (x2, y2) = self.calculate_xy()
        line = [0, x1, x2], [0, y1, y2]

        if i == 0:
            self.trace_x.clear()
            self.trace_y.clear()

        self.trace_x.appendleft(x2)
        self.trace_y.appendleft(y2)

        self.line.set_data(*line)
        self.trace.set_data(self.trace_x, self.trace_y)
        self.time_text.set_text(self.time_template % (i * self.dt))

        return self.line, self.trace, self.time_text

    def animate(self):
        anim = animation.FuncAnimation(
            self.fig, self.animate_func, interval = self.dt * 1000, blit = True)
        plt.show()

def main():
    o1 = Object(mass = 5, length = 2, angle = -pi/2)
    o2 = Object(mass = 7, length = 1.5, angle = -pi/4)

    Pendulum(o1, o2).animate()

if __name__ == '__main__':
    main()
