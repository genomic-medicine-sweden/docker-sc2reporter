import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getNextclade } from '../services/api'
import { SamplesTable } from '../components/SamplesTable'
import { Card } from 'antd'

export const NextcladePage = ({ token, isAdmin }) => {
  const [samples, setSamples] = useState<any>()
  const [refresh, setRefresh] = useState<boolean>(false)
  const { id } = useParams()
  const title = `Nextclade ${id}`

  useEffect(() => {
    if (id)
      getNextclade(token, id).then((response) => {
        setSamples(response.samples)
      })
  }, [id, refresh])

  const refreshSamples = () => {
    setRefresh((prevRefresh) => !prevRefresh)
  }

  return (
    <Card>
      <SamplesTable
        token={token}
        samples={samples}
        refreshSamples={refreshSamples}
        isAdmin={isAdmin}
        title={title}
        subTitle={null}
      />
    </Card>
  )
}
