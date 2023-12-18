import pandas as pd
from pathlib import Path


class WSection:
    cwd = Path(__file__).parent
    E = 206000
    __doc__ = """This progarm can get properties of w-section steel beam
    Axis Definition:
                 ↑y
                 |
           ============
                 ‖
                 ‖        x
         --------‖--------→
                 ‖
                 ‖
           ============
                 |
    d: Depth
    bf: Top width
    tf: Flange thickness
    tw: Web thickness
    r: Fillet radius
    A: Area
    J: Torsion constant
    Iy: Moment of inertia about y-axis
    Ix: Moment of inertia about x-axis
    Alpha: Principal axis angle
    Iw: Warping constant
    Zy: Plastic modulars about y-axis
    Zx: Plastic modulars about x-axis
    (All units are in "mm" or "N")
    """


    def __init__(self, section: str, fy: float=None):
        """get section property with given section name 

        Args:
            section (str): section name
            fy (float, optional): yield strength (Dafault to None).

        Example:
            >>> section = WSection('W14x90', fy=345)
        """
        self.section = section
        try:
            section_data = pd.read_csv(self.cwd / 'W-section.csv')
        except:
            raise FileNotFoundError('"W-section.csv" not found!')
        try:
            data = section_data.loc[section_data['section'] == self.section].iloc[0].tolist()
        except:
            raise ValueError(f'"{self.section}" not found!')
        self.name, self.d, self.bf, self.tf, self._bf_bottom, self._tf_bottom, self.tw, self.r, self.A,\
            self.J, self.Iy, self.Ix, self.Alpha, self.Cy, self.Cx, self.Iw, self.Zy, self.Zx = data
        self.h = self.d - 2 * self.tf - 2 * self.r
        self.ry = (self.Iy / self.A) ** 0.5
        self.rx = (self.Ix / self.A) ** 0.5
        self.Wy = self.Iy / (self.d / 2)
        self.Wx = self.Ix / (self.d / 2)
        if fy:
            self.fy = fy
            self.My = self.fy * self.Wx * 1.1
        

    def __getattr__(self, name):
        if name == 'My' or name == 'fy':
            raise AttributeError('Please define parameter `fy` first.')

    def set_fy(self, fy: int):
        """set yield strength of steel to calculate My.

        Args:
            fy (int): yield strength
        """
        self.fy = fy
        self.My = self.fy * self.Wx * 1.1

    def IMKbeam_modeling(self, L: float, Ls: float, Lb: float, RBS=False,
                     composite_action=False):
        """Calculate the IMK model paremeters to model the plastic hinge behavior

        Args:
            L (float): Member Length
            Ls (float): Shear Span
            Lb (float): Unbraced length
            RBS (bool, optional): Reduced beam section? Defaults to False.
            composite_action (bool, optional): Composite Action Consideration. Defaults to False.

        Returns:
            dict: IMK model parameters
        """
        n = 10
        c1 = 1.0
        c2 = 1.0
        c3 = 25.4
        c4 = 1
        htw = self.h / self.tw
        bftf = self.bf / self.tf / 2
        K = (n + 1) * 6 * self.E * self.Ix / L
        if RBS:
            # RBS
            theta_p = 0.19 * (htw ** -0.314) * (bftf ** -0.100) * (Lb / self.ry) ** -0.185 * (Ls / self.d) ** 0.113 * (
                        c1 * self.d / 533) ** -0.760 * (c2 * self.fy * c4 / 355) ** -0.070
            theta_pc = 9.52 * (htw ** -0.513) * (bftf ** -0.863) * (Lb / self.ry) ** -0.108 * (
                        c2 * self.fy * c4 / 355) ** -0.360
            Lmda = 585 * (htw ** -1.140) * (bftf ** -0.632) * (Lb / self.ry) ** -0.205 * (
                        c2 * self.fy * c4 / 355) ** -0.391
            if not composite_action:
                MyPMy = 1.0
                MyNMy = 1.0
                McMyP = 1.1
                McMyN = 1.1
                theta_y = self.My / (6 * self.E * self.Ix / L)
                theta_p = theta_p - (McMyP - 1.0) * self.My / (6 * self.E * self.Ix / L)
                theta_pc = theta_pc + theta_y + (McMyP - 1.0) * self.My / (6 * self.E * self.Ix / L)
                theta_p_P = theta_p
                theta_p_N = theta_p
                theta_pc_P = theta_pc
                theta_pc_N = theta_pc
                theta_u = 0.2
                D_P = 1.0
                D_N = 1.0
                Res_P = 0.4
                Res_N = 0.4
                c = 1
            else:
                MyPMy = 1.35
                MyNMy = 1.25
                McMyP = 1.30
                McMyN = 1.05
                theta_y = self.My / (6 * self.E * self.Ix / L)
                theta_p_p = theta_p - (McMyP - 1.0) * self.My / (6 * self.E * self.Ix / L)
                theta_p_n = theta_p - (McMyN - 1.0) * self.My / (6 * self.E * self.Ix / L)
                theta_pc_p = theta_pc + theta_y + (McMyP - 1.0) * self.My / (6 * self.E * self.Ix / L)
                theta_pc_n = theta_pc + theta_y + (McMyN - 1.0) * self.My / (6 * self.E * self.Ix / L)
                theta_p_P = 1.80 * theta_p_p
                theta_p_N = 0.95 * theta_p_n
                theta_pc_P = 1.35 * theta_pc_p
                theta_pc_N = 0.95 * theta_pc_n
                theta_u = 0.2
                D_P = 1.15
                D_N = 1.0
                Res_P = 0.3
                Res_N = 0.2
        else:
            # other-than-RBS
            if self.d > c3 * 21.0:
                theta_p = 0.318 * (htw ** -0.550) * (bftf ** -0.345) * (Lb / self.ry) ** -0.023 * (Ls / self.d) ** 0.090 * (
                            c1 * self.d / 533) ** -0.330 * (c2 * self.fy * c4 / 355) ** -0.130
                theta_pc = 7.500 * (htw ** -0.610) * (bftf ** -0.710) * (Lb / self.ry) ** -0.110 * (
                            c1 * self.d / 533) ** -0.161 * (c2 * self.fy * c4 / 355) ** -0.320
                Lmda = 536 * (htw ** -1.260) * (bftf ** -0.525) * (Lb / self.ry) ** -0.130 * (
                            c2 * self.fy * c4 / 355) ** -0.291
            else:
                theta_p = 0.0865 * (htw ** -0.360) * (bftf ** -0.140) * (Ls / self.d) ** 0.340 * (
                            c1 * self.d / 533) ** -0.721 * (c2 * self.fy * c4 / 355) ** -0.230
                theta_pc = 5.6300 * (htw ** -0.565) * (bftf ** -0.800) * (
                            c1 * self.d / 533) ** -0.280 * (c2 * self.fy * c4 / 355) ** -0.430
                Lmda = 495 * (htw ** -1.340) * (bftf ** -0.595) * (
                            c2 * self.fy * c4 / 355) ** -0.360
            if not composite_action:
                MyPMy = 1.0
                MyNMy = 1.0
                McMyP = 1.1
                McMyN = 1.1
                theta_y = self.My / (6 * self.E * self.Ix / L)
                theta_p_P = theta_p
                theta_p_N = theta_p
                theta_pc_P= theta_pc
                theta_pc_N = theta_pc
                theta_u = 0.2
                D_P = 1.0
                D_N = 1.0
                Res_P = 0.4
                Res_N = 0.4
                c = 1.0
            else:
                MyPMy = 1.35
                MyNMy = 1.25
                McMyP = 1.30
                McMyN = 1.05
                theta_y = self.My / (6 * self.E * self.Ix / L)
                theta_p_p = theta_p - (McMyP - 1.0) * self.My / (6 * self.E * self.Ix / L)
                theta_p_n = theta_p - (McMyN - 1.0) * self.My / (6 * self.E * self.Ix / L)
                theta_pc_p = theta_pc + theta_y + (McMyP - 1.0) * self.My / (6 * self.E * self.Ix / L)
                theta_pc_n = theta_pc + theta_y + (McMyN - 1.0) * self.My / (6 * self.E * self.Ix / L)
                theta_p_P = 1.80 * theta_p_p
                theta_p_N = 0.95 * theta_p_n
                theta_pc_P = 1.35 * theta_pc_p
                theta_pc_N = 0.95 * theta_pc_n
                theta_u = 0.2
                D_P = 1.15
                D_N = 1.00
                Res_P = 0.3
                Res_N = 0.2
                c = 1.0
        My_P = MyPMy * self.My
        My_N = MyNMy * self.My
        L_S, L_C, L_A, L_K = Lmda, Lmda, Lmda, Lmda
        c_S, c_C, c_A, c_K = c, c, c, c
        result = {
            'K': K, 
            'theta_p_P': theta_p_P,
            'theta_pc_P': theta_pc_P,
            'theta_u': theta_u,
            'My_P': My_P,
            'McMyP': McMyP,
            'Res_P': Res_P,
            'theta_p_N': theta_p_N,
            'theta_pc_N': theta_pc_N,
            'theta_u': theta_u,
            'My_N': My_N,
            'McMyN': McMyN,
            'Res_N': Res_N,
            'L_S': L_S,
            'L_C': L_C,
            'L_K': L_K,
            'c_S': c_S,
            'c_C': c_C,
            'c_K': c_K,
            'D_P': D_P,
            'D_N': D_N
        }
        return result


    def IMKcolumn_modeling(self, L: float, Lb: float, PgPye: float):
        """Calculate the IMK model paremeters to model the plastic hinge behavior

        Args:
            L (float): Member Length
            Lb (float): Unbraced length
            PgPye (float): Axial load ratio due to gravity.

        Returns:
            dict: IMK model parameters
        """
        n = 10
        c1 = 1.0
        c2 = 1.0
        c3 = 25.4
        c4 = 1000.0
        htw = self.h / self.tw
        bftf = self.bf / self.tf / 2
        K = (n + 1) * 6 * self.E * self.Ix / L
        theta_p = 294 * (htw ** -1.700) * (Lb / self.ry) ** -0.700 * (1 - PgPye) ** 1.600
        theta_pc = 90 * (htw ** -0.800) * (Lb / self.ry) ** -0.800 * (1 - PgPye) ** 2.500
        if theta_p > 0.20:
            theta_p = 0.2
        if theta_pc > 0.30:
            theta_pc = 0.3
        if PgPye <= 0.35:
            Lmda = 25500 * (htw ** -2.140) * (Lb / self.ry) ** -0.530 * (1 - PgPye) ** 4.920
        else:
            Lmda = 268000 * (htw ** -2.300) * (Lb / self.ry) ** -1.300 * (1 - PgPye) ** 1.190
        if PgPye <= 0.2:
            My = (1.15 / 1.1) * self.My * (1 - PgPye / 2)
        else:
            My = (1.15 / 1.1) * self.My * (9 / 8) * (1 - PgPye)
        McMy = 12.5 * (htw ** -0.200) * (Lb / self.ry) ** -0.400 * (1 - PgPye) ** 0.400
        if McMy < 1.0:
            McMy = 1.0
        if McMy > 1.3:
            McMy = 1.3
        MyPMy = 1.0
        MyNMy = 1.0
        McMyP = McMy
        McMyN = McMy
        theta_y = My / (6 * self.E * self.Ix / L)
        theta_p = theta_p - (McMyP - 1.0) * My / (6 * self.E * self.Ix / L)
        theta_pc = theta_pc + theta_y + (McMyP - 1.0) * My / (6 * self.E * self.Ix / L)
        theta_p_P = theta_p
        theta_p_N = theta_p
        theta_pc_P = theta_pc
        theta_pc_N = theta_pc
        theta_u = 0.15
        D_P = 1.0
        D_N = 1.0
        Res_P = 0.5 - 0.4 * PgPye
        Res_N = 0.5 - 0.4 * PgPye
        c = 1.0
        My_P = MyPMy * My
        My_N = MyNMy * My
        L_S, L_C, L_A, L_K = Lmda, 0.9 * Lmda, Lmda, 0.9 * Lmda
        c_S, c_C, c_A, c_K = c, c, c, c
        result = {
            'K': K, 
            'theta_p_P': theta_p_P,
            'theta_pc_P': theta_pc_P,
            'theta_u': theta_u,
            'My_P': My_P,
            'McMyP': McMyP,
            'Res_P': Res_P,
            'theta_p_N': theta_p_N,
            'theta_pc_N': theta_pc_N,
            'theta_u': theta_u,
            'My_N': My_N,
            'McMyN': McMyN,
            'Res_N': Res_N,
            'L_S': L_S,
            'L_C': L_C,
            'L_K': L_K,
            'c_S': c_S,
            'c_C': c_C,
            'c_K': c_K,
            'D_P': D_P,
            'D_N': D_N
        }
        return result



if __name__ == "__main__":
    s1 = WSection('W24x84', fy=345)
    print(f'Ix = {s1.Ix}')
    res = s1.IMKbeam_modeling(L=4500, Ls=4500/2, Lb=4500)
    print(res)

    


