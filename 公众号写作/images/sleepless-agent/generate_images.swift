#!/usr/bin/swift

import Foundation
import AppKit

// 设置图片尺寸
let width: CGFloat = 1920
let height: CGFloat = 1080

func createImage(named name: String, drawHandler: (NSGraphicsContext) -> Void) -> NSImage? {
    let image = NSImage(size: NSSize(width: width, height: height))
    image.lockFocus()

    let ctx = NSGraphicsContext.current
    drawHandler(ctx!)

    image.unlockFocus()

    // 保存为 JPG
    let outputPath = "/Users/victoryx/code/document/公众号写作/images/sleepless-agent/\(name)"
    guard let tiffData = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiffData),
          let jpegData = bitmap.representation(using: .jpeg, properties: [.compressionFactor: 0.9]) else {
        return nil
    }

    try? jpegData.write(to: URL(fileURLWithPath: outputPath))
    return image
}

// 颜色辅助函数
func NSColorFromRGB(_ rgb: UInt) -> NSColor {
    let r = CGFloat((rgb >> 16) & 0xFF) / 255.0
    let g = CGFloat((rgb >> 8) & 0xFF) / 255.0
    let b = CGFloat(rgb & 0xFF) / 255.0
    return NSColor(red: r, green: g, blue: b, alpha: 1.0)
}

// 1. 封面图
func createMainCover() -> NSImage? {
    return createImage(named: "01-main.jpg") { ctx in
        // 渐变背景
        let gradient = NSGradient(colors: [
            NSColorFromRGB(0x0A0F1E),
            NSColorFromRGB(0x050A19)
        ])
        gradient?.draw(in: NSRect(x: 0, y: 0, width: width, height: height), angle: 90)

        // 网格线
        NSColor.white.withAlphaComponent(0.05).setStroke()
        for i in stride(from: 0, through: width, by: 100) {
            NSBezierPath.strokeLine(from: NSPoint(x: i, y: 0), to: NSPoint(x: i, y: height))
        }
        for i in stride(from: 0, through: height, by: 100) {
            NSBezierPath.strokeLine(from: NSPoint(x: 0, y: i), to: NSPoint(x: width, y: i))
        }

        // 月亮图标
        let moonRect = NSRect(x: 150, y: 150, width: 200, height: 200)
        NSColorFromRGB(0x283250).setFill()
        NSBezierPath(ovalIn: moonRect).fill()
        NSColorFromRGB(0x6496FF).withAlphaComponent(0.8).setStroke()
        NSBezierPath(ovalIn: moonRect).stroke()

        // AI 核心 (右侧)
        let center: CGFloat = 1400
        let centerY: CGFloat = 300
        for r in stride(from: 150, through: 50, by: -10) {
            let alpha = 1.0 - CGFloat(r) / 150
            NSColorFromRGB(0x0096FF).withAlphaComponent(alpha * 0.3).setFill()
            NSBezierPath(ovalIn: NSRect(x: center - r, y: centerY - r, width: r * 2, height: r * 2)).fill()
        }

        // 标题
        let attrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.boldSystemFont(ofSize: 80),
            .foregroundColor: NSColor.white
        ]
        let title = "Sleepless Agent" as NSString
        title.draw(at: NSPoint(x: width/2 - title.size(withAttributes: attrs).width/2, y: 700), withAttributes: attrs)

        let attrs2: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 40),
            .foregroundColor: NSColorFromRGB(0x64C8FF)
        ]
        let subtitle = "24/7 AI Development Team" as NSString
        subtitle.draw(at: NSPoint(x: width/2 - subtitle.size(withAttributes: attrs2).width/2, y: 800), withAttributes: attrs2)
    }
}

// 2. 多代理工作流图
func createMultiAgentWorkflow() -> NSImage? {
    return createImage(named: "02-multi-agent.jpg") { ctx in
        // 背景
        let gradient = NSGradient(colors: [
            NSColorFromRGB(0x0F1423),
            NSColorFromRGB(0x080C1C)
        ])
        gradient?.draw(in: NSRect(x: 0, y: 0, width: width, height: height), angle: 90)

        // 标题
        let titleAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.boldSystemFont(ofSize: 60),
            .foregroundColor: NSColor.white
        ]
        let title = "Three-Agent Workflow" as NSString
        title.draw(at: NSPoint(x: width/2 - title.size(withAttributes: titleAttrs).width/2, y: 80), withAttributes: titleAttrs)

        // 三个 Agent
        let agents = [
            (x: 320.0, name: "PLANNER", color: NSColorFromRGB(0xFF9632), desc: "分析任务 | 制定计划"),
            (x: 960.0, name: "WORKER", color: NSColorFromRGB(0x32C896), desc: "执行任务 | 编写代码"),
            (x: 1600.0, name: "EVALUATOR", color: NSColorFromRGB(0x6496FF), desc: "验证结果 | 质量检查")
        ]

        for agent in agents {
            // 框
            let rect = NSRect(x: agent.x - 160, y: 250, width: 320, height: 200)
            agent.color.withAlphaComponent(0.15).setFill()
            NSBezierPath(rect: rect).fill()
            agent.color.setStroke()
            NSBezierPath(rect: rect).lineWidth = 4
            NSBezierPath(rect: rect).stroke()

            // 名称
            let nameAttrs: [NSAttributedString.Key: Any] = [
                .font: NSFont.boldSystemFont(ofSize: 36),
                .foregroundColor: agent.color
            ]
            (agent.name as NSString).draw(at: NSPoint(x: agent.x - (agent.name as NSString).size(withAttributes: nameAttrs).width/2, y: 320), withAttributes: nameAttrs)

            // 描述
            let descAttrs: [NSAttributedString.Key: Any] = [
                .font: NSFont.systemFont(ofSize: 24),
                .foregroundColor: NSColor.white.withAlphaComponent(0.8)
            ]
            (agent.desc as NSString).draw(at: NSPoint(x: agent.x - (agent.desc as NSString).size(withAttributes: descAttrs).width/2, y: 370), withAttributes: descAttrs)
        }

        // 连接箭头
        NSColorFromRGB(0x6496C8).setStroke()
        NSBezierPath.strokeLine(from: NSPoint(x: 480, y: 350), to: NSPoint(x: 780, y: 350))
        NSBezierPath.strokeLine(from: NSPoint(x: 1140, y: 350), to: NSPoint(x: 1440, y: 350))
    }
}

// 3. 快速上手图
func createQuickstartGuide() -> NSImage? {
    return createImage(named: "03.5-quickstart.jpg") { ctx in
        let gradient = NSGradient(colors: [
            NSColorFromRGB(0x0C1220),
            NSColorFromRGB(0x060A18)
        ])
        gradient?.draw(in: NSRect(x: 0, y: 0, width: width, height: height), angle: 90)

        let titleAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.boldSystemFont(ofSize: 60),
            .foregroundColor: NSColor.white
        ]
        let title = "Quick Start Guide" as NSString
        title.draw(at: NSPoint(x: width/2 - title.size(withAttributes: titleAttrs).width/2, y: 80), withAttributes: titleAttrs)

        let steps = [
            "1. Install Claude Code CLI",
            "2. Clone Sleepless Agent",
            "3. Install Python Dependencies",
            "4. Create GitHub Token",
            "5. Configure config.yaml",
            "6. Setup GitHub CLI",
            "7. Run First Task",
            "8. Start Daemon (Optional)"
        ]

        let stepAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 28),
            .foregroundColor: NSColorFromRGB(0xC8DCFF)
        ]

        var y: CGFloat = 200
        for step in steps {
            // 圆圈
            let circleRect = NSRect(x: 150, y: y - 25, width: 50, height: 50)
            NSColorFromRGB(0x0096FF).setFill()
            NSBezierPath(ovalIn: circleRect).fill()

            // 步骤文字
            (step as NSString).draw(at: NSPoint(x: 220, y: y - 10), withAttributes: stepAttrs)
            y += 90
        }
    }
}

// 4. 适用场景图
func createScenarios() -> NSImage? {
    return createImage(named: "03-scenarios.jpg") { ctx in
        let gradient = NSGradient(colors: [
            NSColorFromRGB(0x0A101E),
            NSColorFromRGB(0x050A19)
        ])
        gradient?.draw(in: NSRect(x: 0, y: 0, width: width, height: height), angle: 90)

        let titleAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.boldSystemFont(ofSize: 60),
            .foregroundColor: NSColor.white
        ]
        let title = "When to Use Sleepless Agent" as NSString
        title.draw(at: NSPoint(x: width/2 - title.size(withAttributes: titleAttrs).width/2, y: 60), withAttributes: titleAttrs)

        // 左侧适合的
        let leftTitleAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.boldSystemFont(ofSize: 40),
            .foregroundColor: NSColorFromRGB(0x64FF96)
        ]
        let leftTitle = "✅ Great For" as NSString
        leftTitle.draw(at: NSPoint(x: 480 - leftTitle.size(withAttributes: leftTitleAttrs).width/2, y: 180), withAttributes: leftTitleAttrs)

        let itemAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 26),
            .foregroundColor: NSColorFromRGB(0xB4E6C8)
        ]

        let suitable = [
            "Side Projects",
            "• Ideas while sleeping",
            "• Nightly code generation",
            "",
            "Technical Debt",
            "• Add tests",
            "• Refactor code",
            "• Update docs",
            "",
            "Batch Tasks",
            "• License headers",
            "• API migrations"
        ]

        var y: CGFloat = 250
        for item in suitable {
            (item as NSString).draw(at: NSPoint(x: 200, y: y), withAttributes: itemAttrs)
            y += 45
        }

        // 右侧不适合的
        let rightTitleAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.boldSystemFont(ofSize: 40),
            .foregroundColor: NSColorFromRGB(0xFF6464)
        ]
        let rightTitle = "❌ Not For" as NSString
        rightTitle.draw(at: NSPoint(x: 1440 - rightTitle.size(withAttributes: rightTitleAttrs).width/2, y: 180), withAttributes: rightTitleAttrs)

        let notAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 26),
            .foregroundColor: NSColorFromRGB(0xE6B4B4)
        ]

        let notSuitable = [
            "Enterprise Projects",
            "• Complex workflows",
            "• Multi-team collab",
            "",
            "High Interaction",
            "• Frequent changes",
            "• Real-time feedback",
            "",
            "Custom Logic",
            "• Business-specific"
        ]

        y = 250
        for item in notSuitable {
            (item as NSString).draw(at: NSPoint(x: 1100, y: y), withAttributes: notAttrs)
            y += 45
        }
    }
}

// 5. 结尾图
func createConclusion() -> NSImage? {
    return createImage(named: "04-conclusion.jpg") { ctx in
        let gradient = NSGradient(colors: [
            NSColorFromRGB(0x080E1C),
            NSColorFromRGB(0x030816)
        ])
        gradient?.draw(in: NSRect(x: 0, y: 0, width: width, height: height), angle: 90)

        // 装饰点
        for _ in 0..<50 {
            let x = CGFloat.random(in: 0...width)
            let y = CGFloat.random(in: 0...height)
            let size = CGFloat.random(in: 2...6)
            NSColorFromRGB(0x64B4FF).withAlphaComponent(0.3).setFill()
            NSBezierPath(ovalIn: NSRect(x: x, y: y, width: size, height: size)).fill()
        }

        let titleAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.boldSystemFont(ofSize: 70),
            .foregroundColor: NSColor.white
        ]
        let title = "The Future of Development" as NSString
        title.draw(at: NSPoint(x: width/2 - title.size(withAttributes: titleAttrs).width/2, y: 300), withAttributes: titleAttrs)

        let subtitleAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 36),
            .foregroundColor: NSColorFromRGB(0x96C8FF)
        ]

        let line1 = "AI isn't replacing you." as NSString
        line1.draw(at: NSPoint(x: width/2 - line1.size(withAttributes: subtitleAttrs).width/2, y: 420), withAttributes: subtitleAttrs)

        let line2 = "It's becoming your team." as NSString
        line2.draw(at: NSPoint(x: width/2 - line2.size(withAttributes: subtitleAttrs).width/2, y: 480), withAttributes: subtitleAttrs)

        // 分隔线
        NSColorFromRGB(0x5096DC).setStroke()
        NSBezierPath.strokeLine(from: NSPoint(x: 560, y: 560), to: NSPoint(x: 1360, y: 560))

        let textAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 36),
            .foregroundColor: NSColorFromRGB(0xB4C8E6)
        ]
        let text = "You define requirements → AI builds → You review" as NSString
        text.draw(at: NSPoint(x: width/2 - text.size(withAttributes: textAttrs).width/2, y: 680), withAttributes: textAttrs)

        let smallAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 28),
            .foregroundColor: NSColorFromRGB(0x78AAD0)
        ]
        let small = "This is human-AI collaboration, done right." as NSString
        small.draw(at: NSPoint(x: width/2 - small.size(withAttributes: smallAttrs).width/2, y: 780), withAttributes: smallAttrs)

        let linkAttrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 28),
            .foregroundColor: NSColorFromRGB(0x64B4FF)
        ]
        let link = "github.com/context-machine-lab/sleepless-agent" as NSString
        link.draw(at: NSPoint(x: width/2 - link.size(withAttributes: linkAttrs).width/2, y: 900), withAttributes: linkAttrs)
    }
}

// 执行生成
print("Generating images...")
_ = createMainCover()
print("✓ 01-main.jpg")
_ = createMultiAgentWorkflow()
print("✓ 02-multi-agent.jpg")
_ = createQuickstartGuide()
print("✓ 03.5-quickstart.jpg")
_ = createScenarios()
print("✓ 03-scenarios.jpg")
_ = createConclusion()
print("✓ 04-conclusion.jpg")
print("\n✅ All images generated!")
