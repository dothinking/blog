import autograd.numpy as np
from autograd import grad
from ode import ode
from scipy.integrate import odeint

class BicycleTrack(object):
    '''
        Solving and  plot back wheel track according to front wheel track and 
        initial position of the bicycle.

        The track of front wheel is given by:
            x = fx(t)
            y = fy(t)

        Arguments:
            fx  : function object of front wheel track x component
            fy  : function object of front wheel track y component
    ''' 
    def __init__(self, fx, fy):

        # front wheel track and first derivative on parameter t
        self.front_track_x = fx
        self.front_track_y = fy

        self.dfx = grad(fx)
        self.dfy = grad(fy)

        # solved back track represented with t, x, y
        self.t, self.X, self.Y = None, None, None
        self.FX, self.FY = None, None


    def governing_equation(self, t, Y):
        ''' ODEs of Bicycle Track Problem '''
        x, y = Y
        k1 = np.array([self.dfx(t), self.dfy(t)])
        k2 = np.array([x-self.front_track_x(t), y-self.front_track_y(t)])        
        return np.sum(k1*k2) * k2 / self.L**2

    
    def solve(self, span, P0, err=1e-6):
        ''' 
            solve back wheel track according to front wheel track and 
            initial position of the bicycle.

            Arguments:
                span: solving range of parameter t
                P0  : initial position of back wheel (x, y)
        '''

        t0, t1 = span

        # initial point of back wheel
        P0 = np.array(P0)

        # initial point of front wheel is defined by parametric equations
        Q0 = np.array([self.front_track_x(t0), self.front_track_y(t0)])

        # frame length is defined by P0 and Q0
        self.L = np.sum((P0-Q0)**2)**0.5

        # solving
        res = ode(self.governing_equation, span, P0, err=err)

        # solved back track
        XY = [P[1] for P in res]
        X, Y = zip(*XY)
        self.X, self.Y = np.array(X), np.array(Y)

        # front wheel track
        self.t = np.array([P[0] for P in res])
        self.FX, self.FY = self.front_track_x(self.t), self.front_track_y(self.t)


    def plot(self, plt, front_style='-', front_color='deepskyblue', back_style='-', back_color='tomato'):
        ''' Plot front / back wheel tracks '''

        assert self.t is not None, 'No results to plot'

        # tracks
        plt.plot(self.FX, self.FY, front_style, color=front_color, linewidth=1,label='$Front Wheel Track$')
        plt.plot(self.X, self.Y, back_style, color=back_color, linewidth=1, label='$Back Wheel Track$')
        plt.xlabel('$x$')
        plt.ylabel('$y$')
        plt.legend()
        plt.axis('equal')


    def animate(self, plt, animation, front_color='deepskyblue', back_color='tomato'):
        '''
            Plot track animation:
            1) update bicycle position
            2) update passed track
        '''

        # solved tracks in background
        fig = plt.figure(tight_layout=True)
        self.plot(plt, '--', 'lightgray', '--', 'lightgray')

        # line components to be updated
        front_track, = plt.plot([], [], color=front_color, linewidth=1)
        back_track, = plt.plot([], [], color=back_color, linewidth=1)

        front, = plt.plot([], [], color ='silver', linewidth=4)
        back, = plt.plot([], [], color ='silver', linewidth=4)

        frame, = plt.plot([], [], 'k', linewidth=1)
        handle, = plt.plot([], [], 'c', linewidth=1)

        plt.legend((front_track, back_track), ('$Front Wheel Track$', '$Back Wheel Track$'))

        # animation
        self.animation = animation.FuncAnimation(fig, 
            self.__update_pos, 
            list(zip(self.X, self.Y, self.FX, self.FY)),
            fargs=((frame, front, back, handle, front_track, back_track),), 
            interval=100)


    def __pos(self, P, Q, tyre_ratio=0.4, handle_ratio=0.5):
        '''
            Solve control points of bicycle illustration 
            based on front wheel center Q(x,y) and back wheel P(x1, y1).

            Return:
                control points of bicycle components, e.g. frame, wheels, handlebar.
        '''

        x, y = Q
        x1, y1 = P

        # length
        r_tyre = tyre_ratio * self.L / 2.0
        r_handle = handle_ratio * self.L / 2.0

        # parallel direction with frame: wheels
        vx, vy = (x-x1)/self.L, (y-y1)/self.L

        # vertical direction to frame: handle bar
        fx, fy = vy, -vx

        # frame:
        frame_pos = ([x, x1], [y, y1])

        # front_wheel:
        front_pos = ([x+r_tyre*vx, x-r_tyre*vx], [y+r_tyre*vy, y-r_tyre*vy])

        # back_wheel:
        back_pos = ([x1+r_tyre*vx, x1-r_tyre*vx], [y1+r_tyre*vy, y1-r_tyre*vy])

        # handlebar:
        handle_pos = ([x+r_handle*fx, x-r_handle*fx], [y+r_handle*fy, y-r_handle*fy])

        return frame_pos, front_pos, back_pos, handle_pos


    def __update_pos(self, PQ, lines):
        ''' 
            Update bicycle position by setting new data.

            Argument:
                P: tuple (x,y,x1,y1) represents coordinates of front and back wheels
                lines: line objects representing bicycle components, e.g. frame, wheel, handlebar

            Return:
                pre-defined line objects
        '''
        x1,y1,x,y = PQ
        frame, front, back, handle, front_track, back_track = lines

        # get new positions
        frame_pos, front_pos, back_pos, handle_pos = self.__pos((x1, y1), (x, y))

        # update bicycle positions
        if frame: frame.set_data(*frame_pos)
        if front: front.set_data(*front_pos)
        if back: back.set_data(*back_pos)
        if handle: handle.set_data(*handle_pos)

        # update tracks
        # the animation is repeating, so needn't to update the track once finished in a loop
        if front_track:
            fx, fy = front_track.get_data()
            # add new track point in the first loop
            fx = np.append(fx, x) if fx.shape[0]<=self.FX.shape[0] else fx
            fy = np.append(fy, y) if fy.shape[0]<=self.FY.shape[0] else fy
            front_track.set_data(fx, fy)

        if back_track:
            bx, by = back_track.get_data()
            bx = np.append(bx, x1) if bx.shape[0]<=self.X.shape[0] else bx
            by = np.append(by, y1) if by.shape[0]<=self.Y.shape[0] else by
            back_track.set_data(bx, by)

        return lines


if __name__ == '__main__':    

    import matplotlib.pyplot as plt
    import matplotlib.animation as animation

    def fx(x):
        return 5+5*np.cos(x)

    def fy(x):
        return 5*np.sin(x)

    span = [-np.pi, np.pi]
    P0 = np.array([-3, 0])

    BT = BicycleTrack(fx, fy)

    fig = plt.figure(tight_layout=True)
    for i in range(4):
        BT.solve(span, np.array([-4-i, 0]), err=1e-6)
        plt.subplot(221+i)
        BT.plot(plt)

    BT.animate(plt, animation)

    plt.show()
