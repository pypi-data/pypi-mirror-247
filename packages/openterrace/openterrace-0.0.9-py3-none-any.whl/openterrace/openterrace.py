# Import OpenTerrace modules
from . import fluid_substances
from . import bed_substances
from . import domains
from . import diffusion_schemes
from . import convection_schemes

# Import common Python modules
import sys
import tqdm
import numpy as np
import matplotlib
import datetime
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from labellines import labelLines, labelLine

class Simulate:
    """OpenTerrace class."""
    def __init__(self, t_end:float=None, dt:float=None, sim_name:str=None):
        """Initialise with various control parameters.

        Args:
            t_end (float): End time in s
            dt (float): Time step size in s
            sim_name (str): Simulation name
        """
        self.t_start = 0
        self.t_end = t_end
        self.dt = dt
        self.coupling = []
        self.flag_coupling = False
        self.sim_name = sim_name

    def createPhase(self, n:int=None, n_other:int=1, type:str=None):
        """Creates a fluid or bed phase.

        Args:
            n (int): Number of discretisations
            n_other (int): Number of discretisations of interacting phase. If you are defining a bed phase within a tank. Then n_other is the number of discretisations of the fluid phase.
            type (str): Simulation name
        """
        return self.Phase(self, n, n_other, type)
        
    def select_coupling(self, fluid_phase:int=None, bed_phase:int=None, h_exp:str=None, h_value:float=None):
        """Selects coupling of a fluid and bed phase

        Args:
            fluid_phase (int): phase number
            bed_phase (int): phase number
            h_exp (str): Predefined function for convective heat transfer
            h_value (float): Convective heat transfer coefficient in W/(m^2 K)
        """
        valid_h_exp = ['constant']
        if h_exp not in valid_h_exp:
            raise Exception("h_exp \'"+h_exp+"\' specified. Valid options for h_exp are:", valid_h_exp)
        
        self.coupling.append({"fluid_phase":fluid_phase, "bed_phase":bed_phase, "h_exp":h_exp, "h_value":h_value})
        self.flag_coupling = True

    def _coupling(self):
        for couple in self.coupling:
            Q = couple['h_value']*self.Phase.instances[couple['bed_phase']].domain.A[-1][-1]*(self.Phase.instances[couple['fluid_phase']].T[0]-self.Phase.instances[couple['bed_phase']].T[:,-1])*self.dt
            self.Phase.instances[couple['bed_phase']].h[:,-1] = self.Phase.instances[couple['bed_phase']].h[:,-1] + Q/(self.Phase.instances[couple['bed_phase']].rho[:,-1] * self.Phase.instances[couple['bed_phase']].domain.V[-1])
            self.Phase.instances[couple['fluid_phase']].h[0] = self.Phase.instances[couple['fluid_phase']].h[0] - (1-self.Phase.instances[couple['fluid_phase']].phi)*(self.Phase.instances[couple['fluid_phase']].domain.V * self.Phase.instances[couple['fluid_phase']].phi) / np.sum(self.Phase.instances[couple['bed_phase']].domain.V) * Q/(self.Phase.instances[couple['fluid_phase']].rho*self.Phase.instances[couple['fluid_phase']].domain.V)

    def run_simulation(self):
        """This is the function full of magic."""
        for t in tqdm.tqdm(np.arange(self.t_start, self.t_end+self.dt, self.dt)):
            for phase_instance in self.Phase.instances:
                phase_instance._save_data(t)
                phase_instance._solve_equations(t, self.dt)
                phase_instance._update_properties()
            if self.flag_coupling:
                self._coupling()

    def generate_plot(self, pos_phase:object=None, data_phase:object=None, parameter:str='T'):
        filename='ot_plot_'+self.sim_name+'_'+pos_phase.type+'_'+data_phase.type+'_'+parameter+'.png'
        x = pos_phase.domain.node_pos

        if pos_phase == data_phase:
            y = np.mean(getattr(data_phase.data, parameter),1)
        else:
            y = np.mean(getattr(data_phase.data, parameter),2)
        times = getattr(data_phase.data, 'time')
        
        if y.shape[1] == 1:
            y = np.append(y, y, 1)

        fig, axes = plt.subplots()
        for i,time in enumerate(times):
            timelabel = u'$%s$' % time
            plt.plot(x, y[i,:].transpose()-273.15, label=timelabel)

        lines = plt.gca().get_lines()
        labelLines(lines, fontsize=8, align=True)

        plt.grid()
        plt.xlabel('Position (m)')
        plt.ylabel(u'$%s_{%s}$ (\u00B0C)' % (parameter, data_phase.type))
        plt.savefig(filename)

    def generate_animation(self, pos_phase:object=None, data_phase:object=None, parameter:str='T'):
        def _update(frame, parameter):
            x = pos_phase.domain.node_pos
            if pos_phase == data_phase:
                y = np.mean(getattr(data_phase.data, parameter),1)
            else:
                y = np.mean(getattr(data_phase.data, parameter),2)
            times = getattr(data_phase.data, 'time')

            if y.shape[1] == 1:
                y = np.append(y, y, 1)
                
            ax.clear()
            ax.set_xlabel('Position (m)')
            ax.set_ylabel(u'$%s_{%s}$ (\u00B0C)' % (parameter, data_phase.type))
            ax.set_xlim(np.min(pos_phase.domain.node_pos), np.max(pos_phase.domain.node_pos))
            ax.set_ylim(np.min(getattr(data_phase.data,parameter)-273.15)-0.05*(np.max(getattr(data_phase.data, parameter)-273.15)), np.max(getattr(data_phase.data, parameter)-273.15)+0.05*(np.max(getattr(data_phase.data, parameter)-273.15)))
            ax.grid()
            ax.plot(x, y[frame,:].transpose()-273.15, color = '#4cae4f')
            ax.set_title('Time: ' + str(np.round(getattr(data_phase.data, 'time')[frame], decimals=2)) + ' s')

        parameter = 'T'
        fig, ax = plt.subplots()
        fig.tight_layout(pad=2)
        filename='ot_ani_'+self.sim_name+'_'+pos_phase.type+'_'+data_phase.type+'_'+parameter+'.gif'
        ani = anim.FuncAnimation(fig, _update, fargs=parameter, frames=np.arange(len(getattr(data_phase.data, parameter))))
        ani.save(filename, writer=anim.PillowWriter(fps=5), progress_callback=lambda i, n: print(f'{data_phase.type}: saving animation frame {i}/{n}'))

    class Phase:
        instances = []
        """Main class to define either the fluid or bed phase."""
        def __init__(self, outer=None, n:int=None, n_other:int=None, type:str=None):
            """Initialise a phase with number of control points and type.

            Args:
                n_self (int): Number of discretisations for the given phase
                n_other (int): Number of discretisations for the other phase
                type (str): Type of phase
            """
            self.outer = outer
            self.__class__.instances.append(self)
            self.n = n
            self.n_other = n_other
            
            self.phi = 1
            self.bcs = []
            self.sources = []

            self._flag_save_data = False
 
            self.type = type
            self._valid_inputs(type)

        def _valid_inputs(self, type:str=None):
            """Gets valid domain and substances depending on type of phase.
            """
            self.valid_domains = globals()['domains'].__all__
            self.valid_substances = globals()[type+'_substances'].__all__

        def select_substance_on_the_fly(self, cp:float=None, rho:float=None, k:float=None):
            """Defines and selects a new substance on-the-fly. This is useful for defining a substance for testing purposes with temperature independent properties.

            Args:
                cp (float): Specific heat capacity in J/(kg K)
                rho (float): Density in kg/m^3
                k (float): Thermal conductivity in W/(m K)
            """
            class dummy:
                pass
            self.fcns = dummy()
            self.fcns.h = lambda T: np.ones_like(T)*T*cp
            self.fcns.T = lambda h: np.ones_like(h)*h/cp
            self.fcns.cp = lambda h: np.ones_like(h)*cp
            self.fcns.k = lambda h: np.ones_like(h)*k
            self.fcns.rho = lambda h: np.ones_like(h)*rho

        def select_substance(self, substance:str=None):
            """Selects one of the predefined substancers.

            Args:
                substance (str): Substance name
            """
            if not substance:
                raise Exception("Keyword 'substance' not specified.")
            if not substance in self.valid_substances:
                raise Exception(substance+" specified as "+self.type+" substance. Valid "+self.type+" substances are:", self.valid_substances)
            self.fcns = getattr(globals()[self.type+'_substances'], substance)

        def select_domain_shape(self, domain:str=None, **kwargs):
            """Select domain shape and initialise constants."""
            kwargs['n'] = self.n
            if not domain:
                raise Exception("Keyword 'domain' not specified.")
            if not domain in globals()['domains'].__all__:
                raise Exception("domain \'"+domain+"\' specified. Valid options for domain are:", self.valid_domains)
            self.domain = getattr(globals()['domains'], domain)
            self.domain.type = domain
            self.domain.validate_input(kwargs, domain)
            self.domain.shape = self.domain.shape(kwargs)
            self.domain.node_pos = self.domain.node_pos(kwargs)
            self.domain.dx = self.domain.dx(kwargs)
            self.domain.A = self.domain.A(kwargs)
            self.domain.V = self.domain.V(kwargs)

        def select_porosity(self, phi:float=1):
            """Select porosity from 0 to 1, e.g. filling the domain with the phase up to a certain degree."""
            self.domain.V = self.domain.V*phi
            self.phi = phi

        def select_schemes(self, diff:str=None, conv:str=None):
            """Imports the specified diffusion and convection schemes."""

            if self.domain.type == 'lumped':
                raise Exception("'lumped' has been selected as domain type. Please don't specify a discretisation scheme.")

            if diff is not None:
                try:
                    self.diff = getattr(getattr(globals()['diffusion_schemes'], diff), diff)
                except:
                    raise Exception("Diffusion scheme \'"+diff+"\' specified. Valid options for diffusion schemes are:", diffusion_schemes.__all__)

            if conv is not None:
                try:
                    self.conv = getattr(getattr(globals()['convection_schemes'], conv), conv)
                except:
                    raise Exception("Convection scheme \'"+conv+"\' specified. Valid options for convection schemes are:", convection_schemes.__all__)

        def select_initial_conditions(self, T:float=None):
            """Initialises temperature and massflow fields"""
            if T is not None:
                self.T = np.tile(T,(np.append(self.n_other,self.domain.shape)))
                self.h = self.fcns.h(self.T)
            self.T = self.fcns.T(self.h)
            self.rho = self.fcns.rho(self.h)
            self.cp = self.fcns.cp(self.h)
            self.k = self.fcns.k(self.h)
            self.D = np.zeros(((2,)+(self.T.shape)))
            self.F = np.zeros(((2,)+(self.T.shape)))
            self.S = np.zeros(self.T.shape)

        def select_massflow(self, mdot:list[float]=None):
            self.mdot_array = np.array(mdot)

        def select_bc(self, bc_type:str=None, parameter:str=None, position=None, value:float=None):
            """Specify boundary condition type"""
            valid_bc_types = ['fixedValue','zeroGradient']
            if bc_type not in valid_bc_types:
                raise Exception("bc_type \'"+bc_type+"\' specified. Valid options for bc_type are:", valid_bc_types)
            valid_parameters = ['T','mdot']
            if parameter not in valid_parameters:
                raise Exception("parameter \'"+parameter+"\' specified. Valid options for parameter are:", valid_parameters)
            if not position:
                raise Exception("Keyword 'position' not specified.")
            if value is None and bc_type=='fixedValue':
                raise Exception("Keyword 'value' is needed for fixedValue type bc.")
            self.bcs.append({'type': bc_type, 'parameter': parameter, 'position': position, 'value': np.array(value)})

        def select_source_term(self, **kwargs):
            valid_source_types = ['thermal_resistance']
            if kwargs['source_type'] not in valid_source_types:
                raise Exception("source_type \'"+kwargs['source_type']+"\' specified. Valid options for source_type are:", valid_source_types)
            if kwargs['source_type'] == 'thermal_resistance':
                required = ['R','T_inf', 'position']
                for var in required:
                    if not var in kwargs:
                        raise Exception("Keyword \'"+var+"\' not specified for source of type \'"+kwargs['source_type']+"\'")
            self.sources.append(kwargs)

        def select_output(self, times:list[float]=None, parameters:list[str]=None):
            class Data(object):
                pass
            self.data = Data()
            self.data.time = np.intersect1d(np.array(times), np.arange(self.outer.t_start, self.outer.t_end+self.outer.dt, self.outer.dt))
            self.data.parameters = parameters
            for parameter in parameters:
                setattr(self.data,parameter, np.full((len(self.data.time), self.n_other, self.n),np.nan))
                self._flag_save_data = True
                self._q = 0

        def _save_data(self, t:float=None):
            if self._flag_save_data:
                if t in self.data.time:
                    self.data.time[self._q] = t
                    for parameter in self.data.parameters: 
                        getattr(self.data,parameter)[self._q] = getattr(self,parameter)
                        self._q = self._q+1

        def _update_massflow_rate(self, t:float=None):
            """Updates mass flow rate"""
            if self.mdot_array.ndim == 0:
                self.mdot = np.tile(self.mdot_array,(np.append(self.n_other,self.domain.shape)))
            elif self.mdot_array.ndim == 2:
                self.mdot = np.interp(t, self.mdot_array[:,0], self.mdot_array[:,1])

        def _update_properties(self):
            """Updates properties based on specific enthalpy"""
            self.T = self.fcns.T(self.h)
            self.rho = self.fcns.rho(self.h)
            self.cp = self.fcns.cp(self.h)

            if hasattr(self, 'diff'):
                self.k = self.fcns.k(self.h)
                self.D[0,:,:] = self.k*self.domain.A[0]/self.domain.dx
                self.D[1,:,:] = self.k*self.domain.A[1]/self.domain.dx

            if hasattr(self, 'conv'):
                self.F[0,:,:] = self.mdot*self.cp
                self.F[1,:,:] = self.mdot*self.cp

        def _update_boundary_nodes(self, t:float=None, dt:float=None):
            """Update boundary nodes"""
            for bc in self.bcs:
                if bc['type'] == 'fixedValue':
                    self.h[bc['position']] = self.fcns.h(bc['value'])
                if bc['type'] == 'fixedValue_timevarying':
                    self.h[bc['position']] = self.fcns.h(np.interp(t,bc['value'][:,0],bc['value'][:,1]))
                if bc['type'] == 'zeroGradient':
                    if bc['position'] == np.s_[:,0]:
                        self.h[bc['position']] = self.h[bc['position']] + (2*self.T[:,1]*self.D[1,:,0] - 2*self.T[:,0]*self.D[1,:,0] - self.F[0,:,1]*self.T[:,1] + self.F[1,:,0]*self.T[:,0]) / (self.rho[:,0]*self.domain.V[0])*dt
                    if bc['position'] == np.s_[:,-1]:
                        self.h[bc['position']] = self.h[bc['position']] + (2*self.T[:,-2]*self.D[0,:,-1] - 2*self.T[:,-1]*self.D[0,:,-1] + self.F[1,:,-2]*self.T[:,-2] - self.F[0,:,-1]*self.T[:,-1]) / (self.rho[:,-1]*self.domain.V[-1])*dt

        def _update_source(self, dt:float=None):
            for source in self.sources:
                if source['source_type'] == 'thermal_resistance':
                    self.h[source['position']] = self.h[source['position']] + (2/source['R'] * (source['T_inf']-self.T[source['position']])) / (self.rho[source['position']]*self.domain.V[source['position'][1]])*dt

        def _solve_equations(self, t:float=None, dt:float=None):
            self._update_boundary_nodes(t, dt)
            if hasattr(self, 'diff'):
                self.h = self.h + self.diff(self.T, self.D)/(self.rho*self.domain.V)*dt
            if hasattr(self, 'conv'):
                self._update_massflow_rate()
                self.h = self.h + self.conv(self.T, self.F)/(self.rho*self.domain.V)*dt
            if self.sources is not None:
                self._update_source(dt)