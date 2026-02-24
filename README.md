Instructions in the notion:https://www.notion.so/Material-Database-Info-31127990d78e8044b66efd866a5d131b
## How to Install Material Database

- Have python installed https://www.python.org/downloads/windows/
- Have git installed https://git-scm.com/download/win
    - Make sure when you install git follow these steps to make sure it is added to path
        1. Run the Git installer downloader 
        2. Click "Next" through the first few default screens.
        3. Stop when you get to the screen titled "Adjusting your PATH environment".
        4. Make sure the middle option is selected: "Git from the command line and also from 3rd-party software."
        5. Click "Next" through the rest of the standard options until the installation finishes.
        6. You must completely close you current Codingwindow.
        7. Open a fresh Coding window.
        8. Type git --version and hit Enter (if version number comes up git is properly installed)
- Have visual studio code installed https://code.visualstudio.com/download
- Have github access to gt-space (ask one of the Engine Dev Code leads for access if you don’t have it)
    1. Open terminal and paste this into line:
        
        pip install "git+https://github.com/gt-space/engine-designer.git#egg=matproplib&subdirectory=engineDesigner_v5.0/matproplib”
        

If that doesn’t work let Tyson Tran know what your specific error is and I’ll see if I can fix it (should be able to find me on teams)

---

## How to Use

### 1. Basic Material Lookup

You can retrieve properties by calling the global database `db`. Necessary for all operations after this and must be done before looking up any material info.

Python Code:

`import matproplib as mp`

`#Access a material from the registry`

`alloy = mp.db.get_material("inconel_718_annealed")`

### 2. Available Materials

To see a full list of what is currently in the database or scroll down this notion:

Python Code:

`print(mp.db.list_materials())`

### 3. Constant Properties

For properties that don't fluctuate with temperature—or those where temperature-specific data isn't available—we have listed them as constants in the 'Currently Available Materials' section.

Python Code:

`#Get a constant property`

`density = alloy.get("density")
print(f"Density: {density} kg/m^3")`

### 4. Temperature-Dependent Queries

For properties like Elastic Modulus or Specific Heat, provide a temperature in Kelvin. The library will interpolate the value based on the underlying data arrays.

Python Code:

`#Get Yield Strength at a specific engine operating temperature`

`temp_k = 800.0
yield_strength = alloy.get("yield_strength", T=temp_k)`

`print(f"Yield Strength at {temp_k}K: {yield_strength / 1e6:.2f} MPa")`

### **5. Accessing Metadata**

Metadata is for non-numeric or non-interpolated info (like "is it magnetic?" or "what is the carbon content?").

- To get a specific metadata value: Use `get_meta("key_name")`.
- To see all metadata at once: You can access the `.metadata` dictionary attribute directly.

Python Code:
`#Access a specific metadata piece
max_temp = fiberglass.get_meta("max_operating_temp")
print(f"Safe Operating Limit: {max_temp} K")

# View all metadata for that material
print(fiberglass.metadata)`

### **6. Accessing Fatigue Curves (S-N Data) (Work In progress not sure this works)**

Fatigue curves (Stress vs. Number of cycles) are typically stored as a `FatigueProfile` object within your material.

- **To get the full object:** Use `material.fatigue`.
- **To get a value from the curve:** Most setups use a `get_cycles(stress)` or `get_limit(n_cycles)` method within that profile.

Python Code:
`#Check if it even has a fatigue profile
if al6061.fatigue:
    # Predict life for a given stress (e.g., 150 MPa)
    stress_pa = 150e6
    cycles = al6061.fatigue.get_cycles(stress_pa)
    print(f"Cycles to failure at 150 MPa: {cycles:.2e}")
else:
    print("No fatigue data registered for this material.")`

## 7. Advanced Usage: Multi-Condition Data

Some materials in **MatPropLib** contain multiple datasets within a single entry to account for different heat treatments or manufacturing conditions.

### 1. The Default Condition

When you perform a standard `get()` call, the library returns the value for the **default_condition** (This is the condition in the material name).

Python Code:
`# Accesses the default "Annealed" data
inc = mp.db.get_material("inconel_625_annealed")
yield_annealed = inc.get("yield_strength", T=300)`

### 2. Accessing Alternate Conditions

To access a specific heat treatment (like **Solution Treated**), you must pass the `condition` argument. This tells the internal interpolation logic to switch to the alternate data array. (Materials with this multi conditon will be listed in Currently Avaliable Materials and have a header, ie. Inconel 625)

Python

`# Accesses the "Solution Treated" data for the same material
yield_sol = inc.get("yield_strength", T=300, condition="Solution Treated")`

---
## Units for Material Properties

All units are in SI units so some of the yields and modulus will be large just to warn you. Individual units are listed below:

**1. Mechanical Properties**
These properties define how the material handles structural loads and deformation.

- `"density"`**kg/m³ (**Mass per unit volume)
- `"yield_strength"`**Pa (**Stress at which plastic deformation begins)
- `"ultimate_strength"`**Pa (**Maximum stress the material can withstand before failing)
- `"elastic_modulus"`**Pa (**Stiffness (Young's Modulus) of the material)
- `"shear_modulus"`**Pa (**Ratio of shear stress to shear strain)
- `"shear_strength"`**Pa (**Maximum shear stress before failure)
- `"poisson_ratio"`**unitless (**Ratio of transverse strain to axial strain)
- `"torsional_modulus"`**Pa (**Resistance to twisting (often used for shafts/turbines))

**2. Thermal Properties**
These are critical for thrust chamber assembly (TCA) heat transfer and expansion calculations.

- `"thermal_conductivity"`**W/m-K (**Ability of the material to conduct heat)
- `"specific_heat"`**J/kg-K (**Heat energy required to raise temperature by 1K)
- `"melting_point"`**K** Temperature at which the material turns to liquid.

**3. Electrical & Specialized Properties**
Used for sensors, instrumentation, and composite-specific design.

- `"electrical_resistivity"`**Ω·m (**Resistance to electrical current flow)
- `"dielectric_constant"`**unitless (**Relative permittivity (insulators/fiberglass))
- `"yield_strength_0deg"`**Pa (**Tensile strength along the fiber axis (Composites))
- `"yield_strength_90deg"`**Pa (**Tensile strength perpendicular to fibers (Composites))

---

## Adding New Materials

For those who want to have the fun task of adding more materials (or if we find more accurate data sheets) follow this guide:

- The material database code is currently located in engine designer v5 under [matproplib](https://github.com/gt-space/engine-designer/blob/master/engineDesigner_v5.0/matproplib/matproplib/database.py) (will update if there is a change)

To change the functions of database go to [core.py](http://core.py) where all the classes are located 

---

To change what is in the database go to [database.py](http://database.py) 

If you want to add a new material use this template(also located on the top of the [database.py](http://database.py) code):

`#===============================================================`

`#NEW MATERIAL TEMPLATE`

`#===============================================================`

`#1. Initialize the Material Container`

`#Name: Common name (e.g., "Titanium 6Al-4V")`

`#Category: Metal, Ceramic, Composite, Plastic, Superalloy`

`#Default Condition: Annealed, Aged, T6, Solution Treated, etc.`

`new_mat = Material(name="INSERT_NAME_HERE", category="General", default_condition="Standard")`

`#------------------------------------------------------------------------`

`#A. MECHANICAL PROPERTIES`

`#Format: [np.array([Temp1, Temp2...]), np.array([Val1, Val2...])]`

`#Note: For constant values, just use a float instead of the lists`

`#------------------------------------------------------------------------`

`new_mat.add_prop("density", 0.0, "kg/m^3")`

`new_mat.add_prop("yield_strength", [
np.array([293.15]), # Temp in Kelvin
np.array([0.0])     # Value in Pa
], "Pa")`

`new_mat.add_prop("ultimate_strength", [
np.array([293.15]),
np.array([0.0])
], "Pa")`

`new_mat.add_prop("elastic_modulus", [
np.array([293.15]),
np.array([0.0])
], "Pa")`

`new_mat.add_prop("shear_modulus", [
np.array([293.15]),
np.array([0.0])
], "Pa")`

`new_mat.add_prop("poisson_ratio", 0.0, "")`

`#------------------------------------------------------------------------`

`#B. THERMAL PROPERTIES`

`#------------------------------------------------------------------------`

`new_mat.add_prop("thermal_conductivity", [
np.array([293.15]),
np.array([0.0])
], "W/m-K")`

`new_mat.add_prop("specific_heat", [
np.array([293.15]),
np.array([0.0])
], "J/kg-K")`

`new_mat.add_prop("cte", [
np.array([293.15]),
np.array([0.0])
], "1/K")`

`new_mat.add_prop("melting_point", 0.0, "K")`

`#------------------------------------------------------------------------`

`#C. ELECTRICAL PROPERTIES` 

`#------------------------------------------------------------------------`

`new_mat.add_prop("electrical_resistivity", [
np.array([293.15]),
np.array([0.0])
], "Ohm-m")`

`#------------------------------------------------------------------------`

`#D. METADATA(Static info - stays as single values)`

`#------------------------------------------------------------------------`

`new_mat.add_meta("carbon_content",      0.0)
new_mat.add_meta("machinability_index", 0.0)
new_mat.add_meta("heat_treatable",      False)
new_mat.add_meta("magnetic",            False)
new_mat.add_meta("weldability",         "Unknown")`

`#------------------------------------------------------------------------`

`#E. FATIGUE DATA (S-N Curves)`

`#Structure: { Temperature_K : [Cycles_Array, Stress_Array_Pa] }`

`#------------------------------------------------------------------------`

`new_mat.add_fatigue({
293.15: [ np.array([1e4, 1e5, 1e6]), np.array([0.0, 0.0, 0.0]) ]
})`

`#------------------------------------------------------------------------`

`#F. REGISTER (Save to Database)`

`#------------------------------------------------------------------------`

`db.add_material(new_mat)`
