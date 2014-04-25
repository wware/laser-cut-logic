// To run tests, do this:
// npm install buster -g    # if you haven't already
// npm link buster          # to use it in this project
// node noodletest.js

var buster = require('buster');
var assert = buster.referee.assert;
var refute = buster.referee.refute;

var noodle = require('./noodle.js');

var p = noodle.vector(1, 2);

buster.testCase('vector', {
    'plus': function() {
        var q = p.plus(noodle.vector(3, 5));
        assert.equals(q.x(), 4);
        assert.equals(q.y(), 7);
    }
    , 'minus': function() {
        var q = p.minus(noodle.vector(3, 5));
        assert.equals(q.x(), -2);
        assert.equals(q.y(), -3);
    }
    , 'dot': function() {
        assert.equals(p.dot(noodle.vector(3, 5)), 13);
    }
    , 'equals': function() {
        assert(p.equals(noodle.vector(1, 2)));
        assert(p.equals(noodle.vector(1.0000000001, 2)));
        refute(p.equals(noodle.vector(3, 5)));
    }
    , 'postscript': function() {
        assert.equals(p.postscript(), '1 2')
    }
});

buster.testCase('path', {
    'postscript': function() {
        var q = noodle.path();
        q.add(p);
        q.add(noodle.vector(3, 5));
        assert.equals(q.postscript(), '1 2 moveto 3 5 lineto');
        var q = noodle.path();
        q.add(p);
        q.add(noodle.vector(3, 5));
        q.add(noodle.vector(3, 1));
        q.close();
        assert.equals(q.postscript(), '1 2 moveto 3 5 lineto 3 1 lineto closepath');
    }
});