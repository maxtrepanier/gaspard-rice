// Author: Maxime Trépanier
// Date: April 5, 2015

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>
#include "scatter.hpp"
#include "save.hpp"

// using namespace std;

bool getArgs(margs &args, int argc, char* argv[]);

// Constants
static const double maxRadius = 6;  // Escape radius
static const double sRadius = 1;  // Sphere radius
static const double sSpacing = 1.000001;  // Sphere spacing (gap)

int main(int argc, char* argv[])
{
    clock_t start;
    double duration = 0;
    margs args;
    bool intersect = true;

    if (!getArgs(args, argc, argv))  // Read entry parameters. If an error occurs, exit.
        return 0;

    GRModel gr(maxRadius);  // Initialize GR model.
    Ray* output = new Ray[args.numX*args.numY];  // Output data

    gr.init3D(sSpacing, sRadius);

    if (args.verbose)
        std::cout << "Computing scattering..." << std::endl;
    start = clock();
    try  // Compute scattering
    {
        for (unsigned i = 0; i < args.numX; ++i)
        {
            for (unsigned int j = 0; j < args.numY; ++j)
            {
                Ray r;  // Convert [i,j] to coordinates

                r.x << -3, args.x1 + (args.x2 - args.x1)*i/args.numX, args.y1 + (args.y2 - args.y1)*j/args.numY;
                r.v << 1, 0, 0;
                for (unsigned int k = 0; k < args.maxstep; ++k)  // While the ray has not escaped, iterate.
                {
                    intersect = gr.iterate(r);
                    if (!intersect)
                        break;
                }
                output[i*args.numY + j] = r;  // Save data.
            }
        }
    }
    catch (const std::string& message)
    {
        std::cout << message << std::endl;
    }

    duration = (clock() - start) /static_cast<double>(CLOCKS_PER_SEC);
    if (args.verbose)
        std::cout << "Time elapsed: " << duration << " s" << std::endl;

    if (args.image)
    {
        if (args.verbose)
            std::cout << "Saving data to image file: " << args.name << std::endl;
        png::image< png::rgb_pixel > img(args.numX, args.numY);
        // Save data in a png file. We use two functions for coloring
        img = projection(img, args, output, maxRadius);
        img.write(args.name.c_str());
    }
    else
    {
        if (args.verbose)
            std::cout << "Saving data to file: " << args.name << std::endl;
        saveData(args, output, maxRadius);  //Save data in a csv file
        if (args.verbose)
            std::cout << "Done." << std::endl;
    }

    delete[] output;

    return 0;
}

//! Read entry parameters.
bool getArgs(margs &args, int argc, char* argv[])
{
    if (argc > 1)
    {
        if (std::string(argv[1]) == "-h")
        {
            std::cout << "usage: gr [-h] [--name] [--corner] [--sampling] [--maxstep] \n\n";
            std::cout << "This program computes exit angle in the scattering model of Gaspard-Rice\n\n";
            std::cout << "Optional arguments:\n";
            std::cout << "\t--name: Output file name (default: data)\n";
            std::cout << "\t--image: save data as a png image (default: to a csv file)\n";
            std::cout << "\t--absorption: absorption coefficient (default: 0)\n";
            std::cout << "\t--corner: Corner position (default: -1 -1 1 1)\n";
            std::cout << "\t--sampling: Number of points on the grid (default: 1000 1000)\n";
            std::cout << "\t--maxstep: Maximal number of iterations (default: 100)\n";
            std::cout << "\t-v: verbose mode\n";
            return false;
        }
        for (int i = 1; i < argc; ++i)
        {
            std::string str(argv[i]);
            if (str == "--name" && i+1 < argc)
                args.name = std::string(argv[++i]);
            else if (str == "--image")
                args.image = true;
            else if (str == "--absorption" && i+1 < argc)
                args.absorption = atof(argv[++i]);
            else if (str == "--corner" && i+4 < argc)
            {
                args.x1 = atof(argv[++i]);
                args.y1 = atof(argv[++i]);
                args.x2 = atof(argv[++i]);
                args.y2 = atof(argv[++i]);
            }
            else if (str == "--sampling" && i+2 < argc)
            {
                args.numX = atoi(argv[++i]);
                args.numY = atoi(argv[++i]);
            }
            else if (str == "--maxstep" && i+1 < argc)
                args.maxstep = atoi(argv[++i]);
            else if (str == "-v")
                args.verbose = true;
            else
            {
                std::cout << "Unknown " << argv[i] << " argument" << std::endl;
                return false;
            }
        }
    }
    return true;
}
