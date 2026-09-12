import AppKit
import Foundation
import Vision

struct Box: Encodable {
    var x: Double
    var y: Double
    var w: Double
    var h: Double
    var yaw: Double
    var roll: Double
    var pitch: Double
    var mouth: Double
}

struct Hand: Encodable {
    var chirality: String
    var open: Double
    var cx: Double
    var cy: Double
    var span: Double
    var thumb: Double
    var index: Double
    var pinky: Double
}

struct Frame: Encodable {
    var path: String
    var w: Int
    var h: Int
    var faces: [Box]
    var hands: [Hand]
}

func vis(_ r: CGRect) -> (Double, Double, Double, Double) {
    (Double(r.origin.x), Double(1 - r.origin.y - r.height), Double(r.width), Double(r.height))
}

func mouthOpen(_ face: VNFaceObservation) -> Double {
    guard let pts = face.landmarks?.outerLips?.normalizedPoints, pts.count >= 4 else { return 0 }
    let ys = pts.map { Double($0.y) }
    let xs = pts.map { Double($0.x) }
    let hh = (ys.max() ?? 0) - (ys.min() ?? 0)
    let ww = (xs.max() ?? 0) - (xs.min() ?? 0)
    return ww > 1e-6 ? min(1, hh / ww) : 0
}

func pt(_ obs: VNHumanHandPoseObservation, _ j: VNHumanHandPoseObservation.JointName) -> CGPoint? {
    (try? obs.recognizedPoint(j)).flatMap { $0.confidence > 0.2 ? $0.location : nil }
}

func dist(_ a: CGPoint, _ b: CGPoint) -> Double {
    hypot(Double(a.x - b.x), Double(a.y - b.y))
}

func one(_ path: String) -> Frame {
    var out = Frame(path: path, w: 0, h: 0, faces: [], hands: [])
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { return out }
    out.w = cg.width
    out.h = cg.height
    let faceReq = VNDetectFaceLandmarksRequest()
    let handReq = VNDetectHumanHandPoseRequest()
    handReq.maximumHandCount = 2
    let hnd = VNImageRequestHandler(cgImage: cg, options: [:])
    try? hnd.perform([faceReq, handReq])
    for case let f as VNFaceObservation in faceReq.results ?? [] {
        let (x, y, w, h) = vis(f.boundingBox)
        out.faces.append(Box(
            x: x, y: y, w: w, h: h,
            yaw: f.yaw?.doubleValue ?? 0,
            roll: f.roll?.doubleValue ?? 0,
            pitch: f.pitch?.doubleValue ?? 0,
            mouth: mouthOpen(f)
        ))
    }
    for case let hp as VNHumanHandPoseObservation in handReq.results ?? [] {
        let wrist = pt(hp, .wrist)
        let mid = pt(hp, .middleMCP) ?? pt(hp, .middleTip)
        let thumb = pt(hp, .thumbTip)
        let index = pt(hp, .indexTip)
        let pinky = pt(hp, .littleTip)
        var xs: [Double] = []
        var ys: [Double] = []
        for p in [wrist, mid, thumb, index, pinky].compactMap({ $0 }) {
            xs.append(Double(p.x))
            ys.append(1 - Double(p.y))
        }
        let scale = (wrist != nil && mid != nil) ? max(dist(wrist!, mid!), 1e-4) : 0.08
        let open: Double
        if let t = thumb, let i = index {
            open = min(1.4, dist(t, i) / scale) / 1.4
        } else {
            open = 0
        }
        let span: Double
        if let t = thumb, let p = pinky {
            span = min(1, dist(t, p) / 0.55)
        } else {
            span = min(1, (xs.max() ?? 0) - (xs.min() ?? 0))
        }
        let side: String
        switch hp.chirality {
        case .left: side = "left"
        case .right: side = "right"
        default: side = "unknown"
        }
        out.hands.append(Hand(
            chirality: side,
            open: open,
            cx: xs.isEmpty ? 0.5 : xs.reduce(0, +) / Double(xs.count),
            cy: ys.isEmpty ? 0.5 : ys.reduce(0, +) / Double(ys.count),
            span: span,
            thumb: thumb != nil ? 1 : 0,
            index: index != nil ? 1 : 0,
            pinky: pinky != nil ? 1 : 0
        ))
    }
    return out
}

var frames: [Frame] = []
for a in CommandLine.arguments.dropFirst() {
    frames.append(one(a))
}
let data = try JSONEncoder().encode(frames)
FileHandle.standardOutput.write(data)
