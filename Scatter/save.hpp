// Author: Maxime Trépanier
// Date: April 21, 2015

#ifndef SAVE_HPP_INCLUDED
#define SAVE_HPP_INCLUDED

#include <png++/png.hpp>
#include <fstream>
#include <sstream>
#include "scatter.hpp"

/*!
 *  \struct margs
 *  \brief Entry arguments
 */
struct margs
{
    std::string name; /*!< Output file name */
    double x1, y1, x2, y2; /*!< Corner position >*/
    unsigned int numX, numY; /*!< Sampling >*/
    unsigned int maxstep; /*!< Maximal number of iterations */
    bool image; /*!< Save data to image or data file */
    bool verbose, gr2d, angle;
    double absorption;

    /*! \brief Constructor */
    margs(void) : name("data"), image(false), verbose(false), gr2d(false), angle(false)
    {
        x1 = y1 = -1;
        x2 = y2 = 1;
        numX = numY = 1000;
        maxstep = 100;
        absorption = 0;
    }
};

//! Export data to a given file
void saveData(const margs& args, Ray* output, double maxRadius);

//! Give a color depending on the exit
png::image< png::rgb_pixel >& projection(png::image< png::rgb_pixel >& img, const margs& args, Ray* output, double maxRadius);

#endif // SAVE_HPP_INCLUDED
