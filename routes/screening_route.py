from middleware.auth_middleware import role_required
from flask import jsonify, request, send_file, Blueprint
from models import User, Screening
from flask_jwt_extended import get_jwt_identity, jwt_required
from schemas.screening_schema import ScreeningSchema, ScreeningAdminSchema
from marshmallow import ValidationError
from app import db, app
from engine import nb_engine, c45_engine


screening_bp = Blueprint("screening", __name__)

def get_result(user_id):
    schema = ScreeningSchema()
    screening = (
        Screening.query.filter_by(user_id=user_id)
        .order_by(Screening.date.desc())
        .first()
    )

    if screening is None:
        return jsonify({"message": "User belum melakukan screening"}), 404

    return jsonify({"screening": schema.dump(screening)})


def add(user_id):
    schema = ScreeningSchema()
    try:
        data = request.get_json()
        data["user_id"] = user_id

        try:
            validated = schema.load(data)
        except ValidationError as err:
            return jsonify({"error": err.messages}), 400

        val = [data["hb"], data["mcv"], data["mch"]]
        result = nb_engine.check_probability(val)
        print(result)
        probability = round(result["probability"], 2)
        prediction = result["prediction"]

        screening = Screening(
            **validated, probability=probability, prediction=prediction
        )

        db.session.add(screening)
        db.session.commit()

        return jsonify({"message": "Screening berhasil", "result": result})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@screening_bp.route("/", methods=["GET"])
@jwt_required()
@role_required("Admin")
def get_all():
    confirmed = request.args.get("confirmed", None)

    schema = ScreeningAdminSchema(many=True)
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    items = Screening.query.order_by(Screening.date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # if confirmed is not None filter dna not null
    if confirmed is not None:
        print(confirmed)
        if confirmed == "true":
            items = (
                Screening.query.filter(Screening.dna != None)
                .order_by(Screening.date.desc())
                .paginate(page=page, per_page=per_page, error_out=False)
            )
        else:
            items = (
                Screening.query.filter(Screening.dna == None)
                .order_by(Screening.date.desc())
                .paginate(page=page, per_page=per_page, error_out=False)
            )

    result = {
        "total_pages": items.pages,
        "current_page": items.page,
        "items_per_page": per_page,
        "total_items": items.total,
        "screenings": schema.dump(items),
    }
    if items.has_next:
        result["next_page"] = items.next_num
    return jsonify(result)


@screening_bp.route("/<screening_id>/update-dna", methods=["PATCH"])
@jwt_required()
def update_dna(screening_id):
    try:
        data = request.get_json()
        screening = Screening.query.get(screening_id)

        if data["dna"] == "null":
            screening.dna = None
            screening.verified = 0
        else:
            screening.dna = int(data["dna"])
            screening.verified = 1

        db.session.commit()
        return jsonify({"message": "Hasil DNA berhasil diubah"})

    except Exception as e:
        print(e)
        return jsonify({"message": "Hasil DNA gagal diubah"}), 500


@screening_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("Admin")
def add_for_user():
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User tidak ditemukan"}), 404

    return add(user_id)


@screening_bp.route("/<user_id>/history", methods=["POST"])
@jwt_required()
def get_histories(user_id):
    schema = ScreeningSchema(many=True)
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    items = (
        Screening.query.filter_by(user_id=user_id)
        .order_by(Screening.date.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    result = {
        "total_pages": items.pages,
        "current_page": items.page,
        "items_per_page": per_page,
        "total_items": items.total,
        "screenings": schema.dump(items),
    }
    if items.has_next:
        result["next_page"] = items.next_num
    return jsonify(result)


@screening_bp.route("/me", methods=["POST"])
@jwt_required()
def add_for_auth_user():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    return add(user.id)


@screening_bp.route("/me", methods=["GET"])
@jwt_required()
def get_result_for_auth_user():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    return get_result(user.id)


@screening_bp.route("/me/history", methods=["GET"])
@jwt_required()
def get_histories_for_auth_user():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    return get_histories(user.id)


# C45
@screening_bp.route("/c45screening", methods=["POST"])
@jwt_required()
def c45():
    # Menerima data dari client
    # req = request.get_json()
    hb = request.json.get("hb")
    mcv = request.json.get("mcv")
    mch = request.json.get("mch")
    nama_model = request.json.get("nama_model")

    # HB,MCV,MCH
    val = [hb, mcv, mch]
    # ubah , jadi .
    val[0] = val[0].replace(',', '.')
    val[1] = val[1].replace(',', '.')
    val[2] = val[2].replace(',', '.')
    # ubah jadi float
    val[0] = float(val[0])
    val[1] = float(val[1])
    val[2] = float(val[2])
    print(val)
    # Melakukan pemrosesan data
    result = c45_engine.cekkemungkinan(val, nama_model)

    return jsonify(
        {
            "success": True,
            "hb": val[0],
            "mcv": val[1],
            "mch": val[2],
            "prediction": result['prediksi'],
            "probability": round(result["probabilitas"], 2),
        }
    )

@screening_bp.route("/make_c45_model", methods=["POST"])
@jwt_required()
def create_c45_model():
    nama_model = request.json.get("name")
    data_periksa = Screening.query.filter_by(verified=1).all()
    c45_engine.create_model(ScreeningSchema(
        many=True).dump(data_periksa), nama_model)
    return jsonify(
        {
            "success": True,
        }
    )
