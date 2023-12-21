from BetterList import BetterList as List
from test import Expect

if __name__ == "__main__":

    expect = Expect("length")
    expect.run(List([1, 2, 5]).length)
    expect.toBe(3)

    expect = Expect("at")
    expect.run(List([1, 2, 5]).at(1))
    expect.toBe(2)

    expect = Expect("map")
    expect.run(List([1, 2, 5]).map(lambda x: x * 2))
    expect.toBe([2, 4, 10])

    expect = Expect("filter")
    expect.run(List([1, 2, 5]).filter(lambda x: x > 2))
    expect.toBe([5])

    expect = Expect("forEach 1")
    temp = []
    List([6, 2, 9]).forEach(lambda val, index: temp.append((val, index)))
    expect.run(temp)
    expect.toBe([(6, 0), (2, 1), (9, 2)])

    expect = Expect("forEach 2")
    temp = []
    List([6, 2, 9]).forEach(
        lambda val: temp.append(val), noIndex=True)
    expect.run(temp)
    expect.toBe([6, 2, 9])

    expect = Expect("concat")
    expect.run(List([1, 2, 5]).concat([3, 4]))
    expect.toBe([1, 2, 5, 3, 4])

    expect = Expect("reduce 1")
    expect.run(List([1, 2, 5]).reduce(lambda x, y: x + y))
    expect.toBe(8)

    expect = Expect("reduce 2")
    expect.run(List([1, 2, 5]).reduce(lambda x, y: x + y, 10))
    expect.toBe(18)

    expect = Expect("reduceRight 1")
    expect.run(List([1, 2, 5]).reduceRight(lambda x, y: x + y))
    expect.toBe(8)

    expect = Expect("reduceRight 2")
    expect.run(List([1, 2, 5]).reduceRight(lambda x, y: x + y, 10))
    expect.toBe(18)

    expect = Expect("find 1")
    expect.run(List([1, 2, 5]).find(lambda x: x > 2))
    expect.toBe(5)

    expect = Expect("find 2")
    expect.run(List([1, 2, 5]).find(lambda x: x > 10))
    expect.toBe(None)

    expect = Expect("findIndex 1")
    expect.run(List([1, 2, 5]).findIndex(lambda x: x > 2))
    expect.toBe(2)

    expect = Expect("findIndex 2")
    expect.run(List([1, 2, 5]).findIndex(lambda x: x > 10))
    expect.toBe(-1)

    expect = Expect("every 1")
    expect.run(List([1, 2, 5]).every(lambda x: x > 2))
    expect.toBe(False)

    expect = Expect("every 2")
    expect.run(List([1, 2, 5]).every(lambda x: x > 0))
    expect.toBe(True)

    expect = Expect("flat", showTimes=True)
    expect._(List([1, 2, 5, [3, 4]]).flat(), [1, 2, 5, 3, 4])
    expect._(List([1, 2, 5, [3, [4]]]).flat(), [1, 2, 5, 3, [4]])
    expect._(List([1, 2, 5, [3, [4]]]).flat(2), [1, 2, 5, 3, 4])
    expect._(List([1, 2, [5, [3, [4]]]]).flat(2), [1, 2, 5, 3, [4]])
    expect._(List([1, 2, [5, [3, [4]]]]).flat(4), [1, 2, 5, 3, 4])

    expect = Expect("fill 1")
    temp = List([1, 2, 5])
    temp.fill(3)
    expect.run(temp)
    expect.toBe([3, 3, 3])

    expect = Expect("fill 2")
    temp = List([1, 2, 5])
    temp.fill(3, 1)
    expect.run(temp)
    expect.toBe([1, 3, 3])

    expect = Expect("fill 3")
    temp = List([1, 2, 5])
    temp.fill(3, 1, 2)
    expect.run(temp)
    expect.toBe([1, 3, 5])

    expect = Expect("copyWithin", showTimes=True)
    expect._(List([1, 2, 3, 4, 5]).copyWithin(0, 3), [4, 5, 3, 4, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(1, 3), [1, 4, 5, 4, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(1, 2), [1, 3, 4, 5, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(2, 2), [1, 2, 3, 4, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(0, 3, 4), [4, 2, 3, 4, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(1, 3, 4), [1, 4, 3, 4, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(1, 2, 4), [1, 3, 4, 4, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(0, -2), [4, 5, 3, 4, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(0, -2, -1), [4, 2, 3, 4, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(-4, -3, -2), [1, 3, 3, 4, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(-4, -3, -1), [1, 3, 4, 4, 5])
    expect._(List([1, 2, 3, 4, 5]).copyWithin(-4, -3), [1, 3, 4, 5, 5])

    expect = Expect("entries", showTimes=True)
    expect._(List(['a', 'b', 'c']).entries(), [(0, 'a'), (1, 'b'), (2, 'c')])
    expect._(List([1, 2, 3]).entries(), [(0, 1), (1, 2), (2, 3)])

    expect = Expect("flatMap", showTimes=True)
    expect._(List([1, 2, 3, 4]).flatMap(
        lambda x: [x, x * 2]), [1, 2, 2, 4, 3, 6, 4, 8])
    expect._(List([1, 2, 3, 4]).flatMap(lambda x: [[x, x * 2]]),
             [[1, 2], [2, 4], [3, 6], [4, 8]])
    expect._(List([1, 2, 3, 4]).flatMap(lambda x: [x, [x * 2]]),
             [1, [2], 2, [4], 3, [6], 4, [8]])

    expect = Expect("from", showTimes=True)
    expect._(List._from([1, 2, 3, 4]), [1, 2, 3, 4])
    expect._(List._from([]), [])

    expect = Expect("includes", showTimes=True)
    expect._(List([1, 2, 3, -0, object]).includes(1), True)
    expect._(List([1, 2, 3, -0, object]).includes(-0), True)
    expect._(List([1, 2, 3, -0, object]).includes(0), True)
    expect._(List([1, 2, 3, -0, object]).includes(object), True)
    expect._(List([1, 2, 3, -0, object]).includes(4), False)
    expect._(List([1, 2, 3, -0, object]).includes(-0.5), False)
    expect._(List([1, 2, 3, -0, object]).includes({}), False)
    expect._(List([1, 2, 3, -0, object]).includes(None), False)
    expect._(List([None]).includes(None), True)

    expect = Expect("indexOf", showTimes=True)
    expect._(List([1, 1, 1]).indexOf(1), 0)
    expect._(List([1, 2, 3]).indexOf(1, 1), -1)
    expect._(List([1, 2, 3]).indexOf(2, 1), 1)
    expect._(List([1, 2, 3]).indexOf(2, -1), -1)
    expect._(List([1, 2, 3]).indexOf(2, -2), 1)
    expect._(List([None]).indexOf(None), 0)

    expect = Expect("isArray", showTimes=True)
    expect._(List.isArray([]), True)
    expect._(List.isArray([1, 2, 3]), True)
    expect._(List.isArray({}), False)
    expect._(List.isArray(None), False)
    expect._(List.isArray(1), False)
    expect._(List.isArray("1"), False)

    expect = Expect("join", showTimes=True)
    expect._(List(['a', 'b', 'c']).join(), "a,b,c")
    expect._(List([1, 2, 3]).join(), "1,2,3")
    expect._(List([1, 2, 3]).join(""), "123")
    expect._(List([1, 2, 3]).join(" "), "1 2 3")
    expect._(List([1, 2, 3]).join("a"), "1a2a3")
    expect._(List([1, 2, 3]).join(None), "1None2None3")

    expect = Expect("keys", showTimes=True)
    expect._(List(['a', 'b', 'c']).keys(), [0, 1, 2])
    expect._(List([1, 2, 3]).keys(), [0, 1, 2])

    expect = Expect("lastIndexOf", showTimes=True)
    expect._(List([1, 2, 3, 4, 5, 6, 7, 8, 9, 1]).lastIndexOf(1), 9)
    expect._(List([1, 2, 3, 4, 5, 6, 7, 8, 9, 1]).lastIndexOf(1, 8), 0)
    expect._(List([1, 2, 3, 4, 5, 6, 7, 8, 1, 9]).lastIndexOf(1, 7), 0)
    expect._(List([1, 2, 3, 4, 5, 6, 7, 8, 1, 9]).lastIndexOf(10), -1)
    expect._(List([1, 2, 3, 4, 5, 6, 7, 8, 9, 1]).lastIndexOf(1, 9), 9)

    expect = Expect("of", showTimes=True)
    expect._(List.of(1, 2, 3, 4), [1, 2, 3, 4])

    expect = Expect("pop", showTimes=True)
    temp = List([1, 2, 3, 4])
    expect._(temp.pop(), 4)
    expect._(temp, [1, 2, 3])

    expect = Expect("push", showTimes=True)
    temp = List([1, 2, 3, 4])
    expect._(temp.push(5), 5)
    expect._(temp, [1, 2, 3, 4, 5])

    expect = Expect("shift", showTimes=True)
    temp = List([1, 2, 3, 4])
    expect._(temp.shift(), 1)
    expect._(temp, [2, 3, 4])

    expect = Expect("slice", showTimes=True)
    expect._(List([1, 2, 3, 4]).slice(), [1, 2, 3, 4])
    expect._(List([1, 2, 3, 4]).slice(1), [2, 3, 4])
    expect._(List([1, 2, 3, 4]).slice(1, 2), [2])
    expect._(List([1, 2, 3, 4]).slice(1, 3), [2, 3])
    expect._(List([1, 2, 3, 4]).slice(1, 4), [2, 3, 4])
    expect._(List([1, 2, 3, 4]).slice(1, 5), [2, 3, 4])
    expect._(List([1, 2, 3, 4]).slice(1, 0), [])
    expect._(List([1, 2, 3, 4]).slice(1, -1), [2, 3])
    expect._(List([1, 2, 3, 4]).slice(1, -2), [2])

    expect = Expect("some", showTimes=True)
    expect._(List([1, 2, 3, 4]).some(lambda x: x > 2), True)
    expect._(List([1, 2, 3, 4]).some(lambda x: x > 4), False)

    expect = Expect("sort", showTimes=True)
    temp = List([1, 3, 2, 4])
    expect._(temp.sort(), [1, 2, 3, 4])
    expect._(temp, [1, 2, 3, 4])
    temp = List([1, 2, 3, 4])
    expect._(temp.sort(lambda x, y: y - x), [4, 3, 2, 1])

    expect = Expect("splice", showTimes=True)
    temp = List([1, 2, 3, 4])
    expect._(temp.splice(), [])
    expect._(temp, [1, 2, 3, 4])
    temp = List([1, 2, 3, 4])
    expect._(temp.splice(1), [2, 3, 4])
    expect._(temp, [1])
    temp = List([1, 2, 3, 4])
    expect._(temp.splice(1, 2), [2, 3])
    expect._(temp, [1, 4])
    temp = List([1, 2, 3, 4])
    expect._(temp.splice(1, 2, 5), [2, 3])
    expect._(temp, [1, 5, 4])
    temp = List([1, 2, 3, 4])
    expect._(temp.splice(1, 2, 5, 6), [2, 3])
    expect._(temp, [1, 5, 6, 4])
    temp = List([1, 2, 3, 4])
    expect._(temp.splice(1, 2, 5, 6, 7), [2, 3])
    expect._(temp, [1, 5, 6, 7, 4])
    temp = List([1, 2, 3, 4])
    expect._(temp.splice(1, 2, 5, 6, 7, 8), [2, 3])
    expect._(temp, [1, 5, 6, 7, 8, 4])
    temp = List([1, 2, 3, 4])

    expect = Expect("toSorted", showTimes=True)
    values = List([1, 10, 21, 2])
    sortedValues = values.toSorted(lambda a, b: a - b)
    expect._(sortedValues, [1, 2, 10, 21])
    expect._(values, [1, 10, 21, 2])

    expect = Expect("toSpliced", showTimes=True)
    arr = List([1, 3, 4, 6])
    expect._(arr.toSpliced(1, 2), [1, 6])

    expect = Expect("toString", showTimes=True)
    expect._(List(['a', 'b', 'c']).toString(), "a,b,c")
    expect._(List([1, 2, 3]).toString(), "1,2,3")

    expect = Expect("unshift", showTimes=True)
    temp = List([1, 2, 3, 4])
    expect._(temp.unshift(5, 6), 6)
    expect._(temp, [5, 6, 1, 2, 3, 4])

    expect = Expect("values", showTimes=True)

    expect = Expect("with", showTimes=True)
    arr = List([1, 2, 3, 4, 5])
    expect._(arr._with(2, 5), [1, 2, 5, 4, 5])
    expect._(arr, [1, 2, 3, 4, 5])
