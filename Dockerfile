# (C) Copyright Banco do Brasil 2019.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limipython3-centos:3.6.8-1

ARG build_date
ARG vcs_ref
ARG VERSAO=1.0.0
ARG BOM_PATH="/docker"

RUN yum update -y
RUN yum install -y gcc gcc-c++ make cmake
ENV CMAKE_C_COMPILER=/usr/bin/gcc CMAKE_CXX_COMPILER=/usr/bin/g++ MODE=prod
RUN yum install -y python36-devel boost-devel libXext libSM libXrender

COPY dist/api_face_detect-${VERSAO}-py3-none-any.whl /
# hadolint ignore=DL3013
RUN pip3 install --upgrade pip
# hadolint ignore=DL3013
RUN pip3 install api_face_detect-${VERSAO}-py3-none-any.whl
RUN rm -fr /api_face_detect-${VERSAO}-py3-none-any.whl

RUN mkdir -p /prometheus

ENV VERSAO=$VERSAO \
    MODE=prod \
    prometheus_multiproc_dir=/prometheus

EXPOSE 9000

WORKDIR /usr/local/lib/python3.6/site-packages/api_face_detect
# Save Bill of Materials to image. Não remova!
COPY README.md CHANGELOG.md LICENSE Dockerfile ${BOM_PATH}/
COPY api_face_detect/config ./config
# Run gunicorn
ENTRYPOINT ["gunicorn", "-c", "config/config.py", "main:app"]
