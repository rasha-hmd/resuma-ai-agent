def should_continue(evaluation):
    try:
        raw_rating = evaluation.get("overall_rating", "")
        rating = float(raw_rating.split("/")[0])
        return rating < 8.5, rating
    except:
        return True, 0.0
