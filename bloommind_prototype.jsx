import React from 'react'

export default function BloomMindPrototype() {
  return (
    <div className="min-h-screen bg-black text-white p-6 space-y-10">
      <HeaderSection />
      <DiaryAndBloomSection />
      <UniverseSection />
      <GrowthSection />
      <MobileBottomNavigation />
    </div>
  )
}

function HeaderSection() {
  return (
    <div className="text-center space-y-4 py-10">
      <h1 className="text-6xl font-bold bg-gradient-to-r from-pink-400 to-yellow-200 text-transparent bg-clip-text">
        思想开花 BloomMind
      </h1>

      <p className="text-xl text-gray-300 max-w-3xl mx-auto">
        AI时代的思想成长平台 · 每个人的第二大脑
      </p>
    </div>
  )
}

function DiaryAndBloomSection() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="bg-zinc-900 rounded-3xl p-6 border border-zinc-800 shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">今日思想日记</h2>
          <span className="text-pink-400">● AI在线</span>
        </div>

        <textarea
          className="w-full h-56 bg-black rounded-2xl p-4 border border-zinc-700"
          placeholder="记录今天的灵感、情绪、成长、创业、想法……"
        />

        <div className="flex gap-3 mt-4 flex-wrap">
          <ActionButton label="🎤 语音输入" />
          <ActionButton label="📷 图片识别" />
          <ActionButton label="⚡ 灵感速记" />

          <button className="px-5 py-3 rounded-2xl bg-gradient-to-r from-pink-500 to-yellow-300 text-black font-bold hover:scale-105 transition">
            🌸 思想开花
          </button>
        </div>
      </div>

      <div className="bg-gradient-to-br from-zinc-900 to-zinc-950 rounded-3xl p-6 border border-pink-500/30 shadow-2xl">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold">AI思想开花结果</h2>
          <div className="animate-pulse text-yellow-300 text-2xl">🌸</div>
        </div>

        <div className="space-y-5">
          <BloomCard
            title="思想总结"
            color="text-pink-400"
            content="你真正焦虑的，并不是工作本身，而是对未来不确定性的失控感。"
          />

          <BloomCard
            title="历史关联"
            color="text-yellow-300"
            content="你当前的状态，与乔布斯离开苹果后的阶段高度相似。"
          />

          <div className="bg-black/40 rounded-2xl p-4 border border-zinc-800">
            <h3 className="text-green-400 mb-2 font-bold">AI成长建议</h3>

            <ul className="list-disc list-inside text-gray-300 space-y-1">
              <li>减少信息输入</li>
              <li>聚焦单一目标</li>
              <li>建立晨间记录习惯</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

function ActionButton({ label }: { label: string }) {
  return (
    <button className="px-5 py-3 rounded-2xl bg-zinc-800 hover:bg-zinc-700 transition">
      {label}
    </button>
  )
}

function BloomCard({
  title,
  color,
  content,
}: {
  title: string
  color: string
  content: string
}) {
  return (
    <div className="bg-black/40 rounded-2xl p-4 border border-zinc-800">
      <h3 className={`${color} mb-2 font-bold`}>
        {title}
      </h3>

      <p className="text-gray-300">{content}</p>
    </div>
  )
}

function UniverseSection() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <InfoCard
        title="思想宇宙"
        items={[
          ['成长指数', '89%'],
          ['情绪稳定度', '72%'],
          ['创造力', '95%'],
        ]}
      />

      <div className="bg-zinc-900 rounded-3xl p-6 border border-zinc-800">
        <h2 className="text-2xl font-bold mb-4">AI知识库</h2>

        <div className="space-y-2">
          {['📚 创业灵感', '💰 财富认知', '🧠 哲学思考', '🔥 情绪成长'].map((item) => (
            <div key={item} className="bg-black rounded-xl p-3">
              {item}
            </div>
          ))}
        </div>
      </div>

      <div className="bg-zinc-900 rounded-3xl p-6 border border-zinc-800">
        <h2 className="text-2xl font-bold mb-4">思想社区</h2>

        <div className="space-y-4">
          <CommunityPost
            user="@成长中的创业者"
            emoji="🌸"
            text="AI今天帮我分析了创业焦虑。"
          />

          <CommunityPost
            user="@自由思想者"
            emoji="✨"
            text="我的日记第一次被AI升华成哲学思考。"
          />
        </div>
      </div>
    </div>
  )
}

function InfoCard({
  title,
  items,
}: {
  title: string
  items: string[][]
}) {
  return (
    <div className="bg-zinc-900 rounded-3xl p-6 border border-zinc-800">
      <h2 className="text-2xl font-bold mb-4">{title}</h2>

      <div className="space-y-3 text-gray-300">
        {items.map(([label, value]) => (
          <div key={label} className="flex justify-between">
            <span>{label}</span>
            <span>{value}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function CommunityPost({
  user,
  emoji,
  text,
}: {
  user: string
  emoji: string
  text: string
}) {
  return (
    <div className="bg-black rounded-2xl p-4">
      <div className="flex justify-between mb-2">
        <span className="font-bold">{user}</span>
        <span>{emoji}</span>
      </div>

      <p className="text-gray-400 text-sm">{text}</p>
    </div>
  )
}

function GrowthSection() {
  return (
    <div className="bg-gradient-to-r from-pink-500/20 to-yellow-300/10 rounded-3xl p-10 border border-pink-500/20">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
        <div>
          <h2 className="text-4xl font-bold mb-4">
            AI人生成长系统
          </h2>

          <p className="text-gray-300 text-lg leading-8">
            思想开花将持续学习你的思想与成长轨迹。
          </p>
        </div>

        <InfoCard
          title="成长数据"
          items={[
            ['连续记录', '128天'],
            ['AI思想分析', '3482次'],
            ['知识库内容', '1286条'],
            ['成长阶段', '爆发期'],
          ]}
        />
      </div>
    </div>
  )
}

function MobileBottomNavigation() {
  const items = [
    { icon: '🏠', label: '首页' },
    { icon: '📚', label: '知识库' },
    { icon: '🌸', label: '开花' },
    { icon: '👥', label: '社区' },
    { icon: '👤', label: '我的' },
  ]

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-zinc-950/90 backdrop-blur-xl border-t border-zinc-800 p-4 flex justify-around z-50">
      {items.map((item) => (
        <button
          key={item.label}
          className="flex flex-col items-center text-gray-400 hover:text-white transition"
        >
          <span className="text-2xl">{item.icon}</span>
          <span className="text-xs mt-1">{item.label}</span>
        </button>
      ))}
    </div>
  )
}

export function AuthPage() {
  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-zinc-900 rounded-3xl p-8 border border-zinc-800 shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-pink-400 to-yellow-200 text-transparent bg-clip-text">
            BloomMind
          </h1>

          <p className="text-gray-400 mt-3">
            登录你的思想宇宙
          </p>
        </div>

        <div className="space-y-4">
          <input
            className="w-full bg-black border border-zinc-700 rounded-2xl p-4"
            placeholder="邮箱地址"
          />

          <input
            type="password"
            className="w-full bg-black border border-zinc-700 rounded-2xl p-4"
            placeholder="密码"
          />

          <button className="w-full bg-gradient-to-r from-pink-500 to-yellow-300 text-black font-bold rounded-2xl p-4">
            登录思想宇宙
          </button>
        </div>
      </div>
    </div>
  )
}
