pkgname=Plan-Imageconverter
pkgver=1.0.0
pkgrel=1
arch=("any")
depends=("python3")
source=("main.py")
makedepends=(python-build python-installer python-wheel)

build() {
    cd "$_name-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$_name-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
}
