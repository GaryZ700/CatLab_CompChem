# Hartree-Fock
A pedagogical focused Hartree-Fock computational chemistry method implementation. The implementation is for closed-shell Hartree-Fock, limited only to hydrogen and helium atoms using guassian s-orbital type basis sets.

# Main Files

## Potential_Energy_Surface
Script that leverages the Hartree-Fock code to compute the 2D potential energy surface for a diatomic molecule composed of hydrogen and/or helium atoms. Example diatomic molecules the script is capable of working with includes diatomic helium, and helium hydride. Due to the calculation being closed-shell, only molecular systems with multiples of two electrons can be computed using this code.  

## Hartree_Fock
General purpose Hartree-Fock code that computes the ground state energy of a diatomic molecule
with a strong focus on demonstrating the overall Hartree-Fock procedure through code and comments.

# Supporting Files

## Hartree_Integrals
Contains a class to compute all the integrals used in the Hartree-Fock approximation, as well as LateX descriptions of the matematics involved in their numerical computation. The integrals included are the overlap, nuclear-nuclear repulsion, electron-nuclear attraction, and electron-electron repulsion integrals.

## Hartree_SCF 
Has support functions used to clean up the SCF code for the Hartree-Fock method, and also provides a general explaination of the SCF portion of the theory.

## Hartree_Class
Contains a class of the hartree-method that can be leveraged to seamlessly run a multitude of simulations one after the other, without needing to be concerned about the inner-workings of the theory.

## molecule
Contains fundamental helper functions for the Hartree-Fock method, including classes to define molecules, atoms, and vectors. Does not contain any pedagogical information.

## morsePotential
Contains a Morse Potential class used to compute an approximate morse potential given the Hartree-Fock
computed potential energy surface data. The method uses a form of the variational method in order to approximate one of the parameters used by the potential.

## notebookImporter
Script that allows for importing python code from one Juypyter Notebook into another notebook.