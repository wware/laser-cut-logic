// http://www.physics.emory.edu/faculty/weeks//graphics/howtops1.html

var epsilon = 1.e-8;

var abs = function(x) {
    return (x < 0) ? -x : x;
};

var vector = function(x, y) {
    return {
        x: function() { return x; }
        , y: function() { return y; }
        , plus: function(other) {
            return vector(x + other.x(), y + other.y());
        }
        , minus: function(other) {
            return vector(x - other.x(), y - other.y());
        }
        , dot: function(other) {
            return x * other.x() + y * other.y();
        }
        , equals: function(other) {
            return abs(x - other.x()) < epsilon && abs(y - other.y()) < epsilon;
        }
        , postscript: function() {
            return '' + x + ' ' + y;
        }
    };
};

var path = function() {
    var closed = false;
    var pieces = [];
    return {
        add: function(vec) {
            if (!closed) {
                pieces.push(vec);
            }
        }
        , close: function() {
            closed = true;
        }
        , postscript: function() {
            if (pieces.length < 2) {
                return;
            }
            var i = 1, r = pieces[0].postscript() + ' moveto';
            while (i < pieces.length) {
                q = pieces[i++];
                r += ' ' + q.postscript() + ' lineto';
            }
            if (closed) {
                r += ' closepath';
            }
            return r;
        }
    }
};

/*
The view specifies a zoom level applicable to both directions,
and offsets in two dimensions.
 */

var grid = function() {
    return {
        postscript: function() {
        }
        , html5canvas: function(view, color) {
            // draw stuff on the canvas
        }
    }
};

module.exports = {
    vector: vector
    , path: path
};