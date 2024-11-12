from app import app
from flask import request, jsonify

@app.route('/api/plates', methods=['GET','POST'])
def data() -> dict:
    """Gets JSON Payload and returns plate optimizations in lbs and kgs and fun units"""
    results = {}

    BAR_LBS_TO_KGS = {
        15: 6.8,
        33: 15,
        45: 20.4,
    }

    # These values are from https://www.roguefitness.com/rogue-olympic-plates
    PLATES_LBS_TO_KGS = {
        1.25: 0.57,
        2.5: 1.13,
        5: 2.3,
        10: 4.5,
        25: 11.3,
        35: 15.9,
        45: 20.4,
        100: 45.4,
    }

    # These are some fun units to compare the totalWeight against
    AVERAGE_WEIGHTS_LBS = {
        "corgis": 27,
        "cats": 10,
        "full kegs": 160,
        "gold bars": 27.4,
    }

    # Gets payload from POST HTTP request
    payload = request.get_json()
    totalWeight:float = payload['totalWeight']
    barWeight:int = payload['barWeight']
    # plateOptions can be unordered. Ordering is handled here.
    availablePlates:list[float] = sorted(payload['plateOptions'], reverse=True)

    # Calculate the number of plates (using lbs)
    results['lbs'] = {}
    platesPerSideLbs = {}
    platesWeightLbs = 0
    remainingWeight = (totalWeight - barWeight) / 2
    for plate in availablePlates:
        numberOfPlates = remainingWeight // plate
        if numberOfPlates > 0 and remainingWeight >=0:
            platesPerSideLbs[plate] = int(numberOfPlates)
            remainingWeight -= numberOfPlates * plate
            platesWeightLbs += 2 * numberOfPlates * plate
    results['lbs']['platesPerSide'] = platesPerSideLbs
    results['lbs']['totalWeight'] = totalWeight
    results['lbs']['barWeight'] = barWeight
    results['lbs']['platesWeight'] = platesWeightLbs

    # Find the equivalent plates in kgs
    results['kgs'] = {}
    platesPerSideKgs = {}
    platesWeightKgs = 0
    for plateLbs, numberOfPlatesLbs in results['lbs']['platesPerSide'].items():
        plateKgs = PLATES_LBS_TO_KGS[plateLbs]
        platesPerSideKgs[plateKgs] = numberOfPlatesLbs
        platesWeightKgs += 2 * numberOfPlatesLbs * plateKgs
    results['kgs']['platesPerSide'] = platesPerSideKgs
    results['kgs']['barWeight'] = BAR_LBS_TO_KGS[barWeight]
    results['kgs']['platesWeight'] = platesWeightKgs
    results['kgs']['totalWeight'] = results['kgs']['barWeight'] + results['kgs']['platesWeight']

    # Find the totalWeight in the various Fun Units
    weightsInFunUnits = {}
    for item, weight in AVERAGE_WEIGHTS_LBS.items():
        multiples = round(totalWeight / weight, 1)
        weightsInFunUnits[item] = multiples
    results['funUnits'] = weightsInFunUnits

    return jsonify(results)