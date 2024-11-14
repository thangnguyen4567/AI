from flask import Blueprint,request,render_template
import json
import english.lambdaTTS as lambdaTTS
import english.lambdaSpeechToScore as lambdaSpeechToScore
import english.lambdaGetSample as lambdaGetSample

english = Blueprint('english', __name__)

@english.route('/test')
def main():
    return render_template('main.html')


@english.route('/getAudioFromText', methods=['POST'])
def getAudioFromText():
    event = {'body': json.dumps(request.get_json(force=True))}
    return lambdaTTS.lambda_handler(event, [])


@english.route('/getSample', methods=['POST'])
def getNext():
    event = {'body':  json.dumps(request.get_json(force=True))}
    return lambdaGetSample.lambda_handler(event, [])


@english.route('/GetAccuracyFromRecordedAudio', methods=['POST'])
def GetAccuracyFromRecordedAudio():

    event = {'body': json.dumps(request.get_json(force=True))}
    lambda_correct_output = lambdaSpeechToScore.lambda_handler(event, [])
    return lambda_correct_output
