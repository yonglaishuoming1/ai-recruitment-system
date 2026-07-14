import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Users, Briefcase, Calendar, TrendingUp } from 'lucide-react'

const stats = [
  { title: '候选人总数', value: '128', icon: Users, change: '+12%' },
  { title: '开放职位', value: '16', icon: Briefcase, change: '+3' },
  { title: '本周面试', value: '24', icon: Calendar, change: '+8%' },
  { title: '录用率', value: '68%', icon: TrendingUp, change: '+5%' },
]

const recentCandidates = [
  { name: '张三', position: '高级前端工程师', status: '面试中', score: 92 },
  { name: '李四', position: '后端架构师', status: '简历筛选', score: 85 },
  { name: '王五', position: '产品经理', status: '已录用', score: 95 },
  { name: '赵六', position: 'UI 设计师', status: '面试中', score: 88 },
]

export function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">仪表盘</h2>
        <p className="text-muted-foreground">招聘管理概览与核心指标</p>
      </div>

      {/* Stats grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.title}
              </CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                {stat.change} 较上月
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent candidates */}
      <Card>
        <CardHeader>
          <CardTitle>最近候选人</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentCandidates.map((candidate) => (
              <div
                key={candidate.name}
                className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0"
              >
                <div>
                  <p className="font-medium">{candidate.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {candidate.position}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <Badge
                    variant={
                      candidate.status === '已录用'
                        ? 'default'
                        : candidate.status === '面试中'
                          ? 'secondary'
                          : 'outline'
                    }
                  >
                    {candidate.status}
                  </Badge>
                  <span className="text-sm font-medium">{candidate.score}分</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
