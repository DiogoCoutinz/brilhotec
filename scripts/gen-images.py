#!/usr/bin/env python3
"""Gera imagens BrilhoTec via kie.ai (Nano Banana 2). Submete em paralelo, faz polling."""
import os, sys, json, time, urllib.request, urllib.error, concurrent.futures, pathlib

API = "https://api.kie.ai/api/v1/jobs"
KEY = os.environ["KIE_API_KEY"]
OUT = pathlib.Path(__file__).parent.parent / "assets" / "img" / "galeria"
OUT.mkdir(parents=True, exist_ok=True)

JOBS = [
    {
        "name": "logo",
        "out": "../logo-brand.png",
        "input": {
            "prompt": "Minimalist vector logo of two stylized abstract buildings drawn in elegant thin gold line strokes on a deep dark navy blue background (#1A2A3F). Two geometric pentagonal building silhouettes side by side, the right one taller with a pointed roof. Pure line-art style, no fill, no shadows, no text, no people. Centered composition, generous padding, professional construction company branding, premium minimal logo design, vector illustration aesthetic. The lines are gold colored #B8794A, crisp and clean.",
            "aspect_ratio": "1:1",
            "resolution": "2K",
            "output_format": "png"
        }
    },
    {
        "name": "hero",
        "out": "../hero-building.jpg",
        "input": {
            "prompt": "Ultra-realistic architectural photography of a beautifully restored modern Portuguese residential building facade at golden hour. Warm sunlight on cream and beige walls, traditional Lisbon architecture with subtle elegant modern details, blue late-afternoon sky, no people visible, professional real estate photography, sharp focus, cinematic depth of field, magazine quality, 35mm photo realism.",
            "aspect_ratio": "4:3",
            "resolution": "2K",
            "output_format": "jpg"
        }
    },
    {
        "name": "pintura-fachada",
        "out": "pintura-fachada.jpg",
        "input": {
            "prompt": "Ultra-photorealistic photograph of a professional painter working on scaffolding painting the facade of a modern Portuguese apartment building. The painter wears clean blue overalls, white helmet and safety harness. Fresh cream-coloured paint visible. Golden hour soft light. Shot from a slight low angle showing both worker and the building scale. Sharp focus on the painter, building extending up. Real photography, high quality DSLR, magazine architectural photography style. No watermarks, no text.",
            "aspect_ratio": "4:3",
            "resolution": "2K",
            "output_format": "jpg"
        }
    },
    {
        "name": "alpinismo",
        "out": "alpinismo-industrial.jpg",
        "input": {
            "prompt": "Ultra-photorealistic dramatic photograph of an industrial rope access technician working high on the facade of a modern building in Portugal. Professional alpinist hanging from ropes with full safety harness, helmet, certified climbing equipment. Shot from below looking up showing the height. Urban Lisbon backdrop, blue sky with light clouds, golden hour lighting. Real photojournalism style, sharp focus, professional DSLR photography, magazine quality. No watermarks, no text overlays.",
            "aspect_ratio": "3:4",
            "resolution": "2K",
            "output_format": "jpg"
        }
    },
    {
        "name": "reabilitacao",
        "out": "reabilitacao-edificio.jpg",
        "input": {
            "prompt": "Ultra-photorealistic photograph of a beautifully renovated traditional Portuguese residential building facade. Fresh cream and warm beige paintwork, restored stone details, immaculate windows, perfectly clean facade against deep blue sky. Architectural photography, frontal symmetric composition, sharp focus, golden hour light, magazine quality real estate photography. No people, no watermarks, no text.",
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "output_format": "jpg"
        }
    },
]

def submit(job):
    body = json.dumps({"model": "nano-banana-2", "input": job["input"]}).encode()
    req = urllib.request.Request(
        f"{API}/createTask",
        data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            j = json.loads(r.read())
            if j.get("code") != 200:
                raise RuntimeError(f"Submit failed: {j}")
            job["taskId"] = j["data"]["taskId"]
            print(f"[submit] {job['name']:18} taskId={job['taskId']}")
            return job
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} submitting {job['name']}: {e.read().decode()}")

def poll(job, timeout=300):
    deadline = time.time() + timeout
    while time.time() < deadline:
        req = urllib.request.Request(
            f"{API}/recordInfo?taskId={job['taskId']}",
            headers={"Authorization": f"Bearer {KEY}"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            j = json.loads(r.read())
        if j.get("code") != 200:
            time.sleep(3); continue
        d = j["data"]
        state = d.get("state")
        if state == "success":
            res = json.loads(d["resultJson"])
            urls = res.get("resultUrls") or res.get("imageUrls") or []
            if not urls:
                raise RuntimeError(f"No URL in resultJson: {d['resultJson']}")
            print(f"[done]   {job['name']:18} → {urls[0]}")
            return urls[0]
        if state in ("fail", "failed"):
            raise RuntimeError(f"{job['name']} failed: {d.get('failMsg')}")
        print(f"[poll]   {job['name']:18} state={state} progress={d.get('progress')}")
        time.sleep(5)
    raise RuntimeError(f"Timeout polling {job['name']}")

def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        dest.write_bytes(r.read())
    print(f"[saved]  {dest.relative_to(pathlib.Path(__file__).parent.parent)}")

def run_one(job):
    try:
        submit(job)
        url = poll(job)
        dest = (OUT / job["out"]).resolve()
        download(url, dest)
        return job["name"], True, str(dest)
    except Exception as e:
        return job["name"], False, str(e)

if __name__ == "__main__":
    print(f"Submitting {len(JOBS)} jobs to kie.ai...\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(JOBS)) as ex:
        results = list(ex.map(run_one, JOBS))
    print("\n=== Results ===")
    fails = 0
    for name, ok, info in results:
        mark = "OK " if ok else "FAIL"
        print(f"{mark}  {name:20} {info}")
        if not ok: fails += 1
    sys.exit(0 if fails == 0 else 1)
