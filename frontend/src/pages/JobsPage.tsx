import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function JobsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">职位管理</h2>
        <p className="text-muted-foreground">管理招聘职位和需求</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>职位列表</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            职位管理功能开发中，敬请期待...
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
