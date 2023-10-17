from flask import jsonify, request, Blueprint
from models import Post
from schemas.posts_schema import PostSchema


post_bp = Blueprint("post", __name__)


@post_bp.route("/news", methods=["GET"])
def get_news():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    
    posts = Post.query.filter(Post.category_id != 2).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    result = {
        "total_pages": posts.pages,
        "current_page": posts.page,
        "items_per_page": per_page,
        "total_items": posts.total,
        "posts": PostSchema(many=True).dump(posts),
    }

    if posts.has_next:
        result["next_page"] = posts.next_num

    return jsonify(result)

# get agenda, category_id = 2
@post_bp.route("/agenda", methods=["GET"])
def get_agenda():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    
    posts = Post.query.filter(Post.category_id == 2).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    result = {
        "total_pages": posts.pages,
        "current_page": posts.page,
        "items_per_page": per_page,
        "total_items": posts.total,
        "posts": PostSchema(many=True).dump(posts), 
    }

    if posts.has_next:
        result["next_page"] = posts.next_num

    return jsonify(result)  


@post_bp.route("/<id>", methods=["GET"])
def get_by_id(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({"message": "Post tidak ditemukan"}), 404

    return jsonify({"post": PostSchema().dump(post)})


@post_bp.route("/static", methods=["GET"])
def get_static():
    posts = Post.query.filter_by(static=True).all()
    if not posts:
        return jsonify({"message": "Informasi tidak ditemukan"}), 404

    return jsonify({"statics": PostSchema(many=True).dump(posts)})
